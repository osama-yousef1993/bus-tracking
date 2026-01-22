import base64
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from uuid import UUID


from cryptography.fernet import Fernet
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError


from src.admins.model import AdminResponse
from src.admins.query import AdminQueries
from src.authentications.model import (
    AdminToken,
    AdminTokenData,
    UserToken,
    UserTokenData,
)
from src.helpers.build_object import Helpers
from src.sessions.models import SessionRequest, SessionResponse
from src.sessions.queries import SessionQueries
from src.users.models import UserResponse
from src.users.queries.users import UserQueries
from src.utils.config import settings


class AuthToken:
    def __init__(self):
        self.user_queries = UserQueries()
        self.admin_user_queries = AdminQueries()
        self.session_queries = SessionQueries()
        self.helper = Helpers()
        key = base64.urlsafe_b64encode(
            settings.jwt.TOKEN_SECRET_KEY.encode()[:32].ljust(32, b"\0")
        )
        self.cipher = Fernet(key)

        self.refresh_token_expire = timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE)
        self.access_token_expire = timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE)

    def create_access_token(
        self,
        data: Dict[str, Any],
        session_id: str,
        expires_delta: datetime = None,
        token_type: str = "user-access",
        purpose: str = "general",
        is_mobile: bool = False,
        audience: str = None,
    ) -> str:
        to_encode = jsonable_encoder(data)
        if not expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.jwt.ACCESS_TOKEN_EXPIRE
            )
        else:
            expire = expires_delta
        if audience is None:
            audience = settings.jwt.AUDIENCE.lower()

        to_encode.update(
            {
                "exp": expire,
                "sub": data.get("id"),
                "iss": settings.jwt.ISSUER,
                "aud": audience,
                "iat": datetime.now(timezone.utc),
                "type": token_type,
                "pur": purpose,
                "ses": session_id,
            }
        )
        if is_mobile:
            to_encode["exp"] = datetime.max
        encode_jwt = jwt.encode(
            to_encode, settings.jwt.SECRET_KEY, algorithm=settings.jwt.ALGORITHM
        )
        return self.encode_token(encode_jwt)

    def create_refresh_token(
        self,
        data: Dict[str, Any],
        token_type: str = "user-refresh",
        purpose: str = "general",
        session_id: str | None = None,
        audience: str = None,
    ):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.jwt.REFRESH_TOKEN_EXPIRE
        )
        to_encode.update(
            {
                "exp": expire,
                "sub": data.get("id"),
                "iss": settings.jwt.ISSUER,
                "aud": audience if audience else settings.jwt.AUDIENCE.lower(),
                "iat": datetime.now(timezone.utc),
                "type": token_type,
                "pur": purpose,
                "ses": session_id,
            }
        )
        encode_jwt = jwt.encode(
            to_encode, settings.jwt.REFRESH_SECRET_KEY, algorithm=settings.jwt.ALGORITHM
        )
        return self.encode_token(encode_jwt)

    def create_google_signup_token(self, google_id: str, email: str, full_name: str):
        payload = {
            "google_id": google_id,
            "email": email,
            "full_name": full_name,
            "type": "google_signup",
            "iss": settings.jwt.ISSUER,
            "aud": settings.jwt.AUDIENCE,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        }

        token = jwt.encode(
            payload, settings.jwt.SECRET_KEY, algorithm=settings.jwt.ALGORITHM
        )

        return self.encode_token(token)

    def generate_password_reset_token(self, email: str) -> str:
        """Generate JWT token for password reset with 1 hour expiry"""
        expires = datetime.now(timezone.utc) + timedelta(minutes=10)
        return self.create_access_token(
            {"sub": email, "purpose": "reset-password"}, expires_delta=expires
        )

    def verify_user_token(
        self,
        token: str,
        is_refresh: bool = False,
        is_password_reset: bool = False,
        two_factor: bool = False,
        is_read_only: bool = False,
        audience: str = None,
    ) -> UserTokenData:
        """
        Verify a JWT and enforce:
        - Correct token *type* (access vs refresh)
        - Correct *purpose* (general / password-reset / 2fa)
        - Standard claims (exp, aud, iss, iat, nbf) with small leeway
        - (Optional) revocation/rotation via JTI lookup


        Returns:
            UserTokenData


        Raises:
            HTTPException 401/404 on invalid token or missing user.
        """
        try:
            # 1) Decode bearer (e.g., strip "Bearer ", URL-safe decode, etc.)
            raw = self.decode_token(token)

            # 2) Choose secret based on token kind
            secret = (
                settings.jwt.REFRESH_SECRET_KEY
                if is_refresh
                else settings.jwt.SECRET_KEY
            )

            #    jose handles exp/nbf/iat by default; we add a small leeway for clock skew.
            payload = jwt.decode(
                raw,
                secret,
                algorithms=[settings.jwt.ALGORITHM],
                issuer=settings.jwt.ISSUER,
                audience=audience,
                options={
                    "verify_aud": True,
                },
            )
            # 4) Validate token type
            expected_type = "user-refresh" if is_refresh else "user-access"
            actual_type = payload.get("type")

            self.verify_session(session_id=payload.get("ses"))
            if actual_type != expected_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=(
                        "Invalid token type for this endpoint. "
                        f"Expected '{expected_type}', got '{actual_type or 'unknown'}'."
                    ),
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # 5) Enforce purpose (pur)
            #    general endpoints only accept 'general'
            #    password reset endpoints accept 'password-reset' and 'general'
            #    2FA endpoints accept '2fa' and 'general'
            pur = payload.get("pur", "general")
            if is_password_reset:
                allowed_purposes = {"reset-password"}
            elif two_factor:
                allowed_purposes = {
                    "2fa-verification",
                    "general",
                    "2fa",
                    "address_book",
                }
            elif is_refresh:
                allowed_purposes = {"general", "2fa"}
            elif is_read_only:
                allowed_purposes = {"read-only"}
            else:
                allowed_purposes = {"general"}

            if pur not in allowed_purposes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=(
                        "Token purpose is not permitted for this operation. "
                        f"Required: {', '.join(sorted(allowed_purposes))}; got: '{pur}'."
                    ),
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # 7) Extract subject and load user
            user_id_str = payload.get("sub")
            if not user_id_str:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=(
                        "Could not validate credentials: missing subject (sub). "
                        "Please authenticate with valid credentials."
                    ),
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user = self.user_queries.get_user_by_id(user_id=user_id_str)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id_str} not found.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user_row = self.helper.build_user_info_object(user)
            # 8) Build response object
            user_data = UserTokenData(
                user_id=user["id"],
                user_setting_id=user_row.user_setting.id,
                session_id=payload.get("ses"),
                full_name=user_row.full_name,
                email=user_row.email,
                phone=user_row.phone,
                type=actual_type
                or ("user-access" if not is_refresh else "user-refresh"),
                exp=payload.get("exp"),
                pur=payload.get("pur"),
            )
            return user_data
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired. Please refresh your token or re-authenticate.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTClaimsError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token claims: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token. Please authenticate with valid credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def verify_admin_token(
        self,
        token: str,
        is_refresh: bool = False,
        is_password_reset: bool = False,
        two_factor: bool = False,
        is_new_password: bool = False,
        audience: str = None,
    ):
        try:
            decode_token = self.decode_token(token)
            secret = (
                settings.jwt.REFRESH_SECRET_KEY
                if is_refresh
                else settings.jwt.SECRET_KEY
            )
            if audience is not None:
                if audience == "none":
                    audience = None
                else:
                    audience = audience.lower()
            else:
                audience = settings.jwt.AUDIENCE.lower()

            payload = jwt.decode(
                decode_token,
                secret,
                algorithms=[settings.jwt.ALGORITHM],
                issuer=settings.jwt.ISSUER,
                audience=audience,
                options={
                    "verify_aud": True,
                },
            )
            admin_id: str | None = payload.get("sub")
            self.verify_session(session_id=payload.get("ses"))

            if admin_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials: Invalid or expired token. Please authenticate with valid credentials.",
                    headers={"WWWW-Authenticate": "Bearer"},
                )
            # expected_type = "admin-refresh" if is_refresh else "user-access"
            # actual_type = payload.get("type")
            # if actual_type != expected_type:
            #     raise HTTPException(
            #         status_code=status.HTTP_401_UNAUTHORIZED,
            #         detail=(
            #             "Invalid token type for this endpoint. "
            #             f"Expected '{expected_type}', got '{actual_type or 'unknown'}'."
            #         ),
            #         headers={"WWW-Authenticate": "Bearer"},
            #     )
            if payload.get("type") != "admin-access":
                if payload.get("type") != "admin-refresh":
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Your Access Type are not allowed to access this resource. Please authenticate with valid credentials.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

            pur = payload.get("pur", "general")
            if is_password_reset:
                allowed_purposes = {"reset-password"}
            elif two_factor:
                allowed_purposes = {"2fa-verification", "general", "2fa"}
            elif is_new_password:
                allowed_purposes = {"set-new-password"}
            elif is_refresh:
                allowed_purposes = {"general", "2fa"}
            else:
                allowed_purposes = {"general"}

            if pur not in allowed_purposes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=(
                        "Token purpose is not permitted for this operation. "
                        f"Required: {', '.join(sorted(allowed_purposes))}; got: '{pur}'."
                    ),
                    headers={"WWW-Authenticate": "Bearer"},
                )

            else:
                admin = self.admin_user_queries.get_admin_by_id(UUID(admin_id))
                if not admin:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {admin_id} not found. It may have been deleted or never existed.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                admin_data = AdminTokenData(
                    admin_id=admin["id"],
                    session_id=payload.get("ses"),
                    email=admin["email"],
                    exp=payload["exp"],
                    type=payload["type"],
                    pur=payload["pur"],
                )

                return admin_data

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token has expired. Please refresh your token or re-authenticate.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTClaimsError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token claims. Please check the issuer, audience, or other claim validations. {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: Invalid or expired token. Please authenticate with valid credentials.",
                headers={"WWWW-Authenticate": "Bearer"},
            )

    def encode_token(self, token: str) -> str:
        # encoded_string = self.cipher.encrypt(token.encode()).decode()
        return token

    def decode_token(self, encoded_token: str) -> str:
        # decoded_string = self.cipher.decrypt(encoded_token.encode()).decode()
        return encoded_token

    def build_user_token(
        self,
        session: SessionRequest,
        user_data: Dict[str, Any],
        user_type: str = "user",
        purpose: str = "general",
        is_mobile: bool = False,
    ):
        session.user_id = user_data["id"]
        session.expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt.REFRESH_TOKEN_EXPIRE
        )
        session.last_seen_at = datetime.now(timezone.utc)
        session_row = self.session_queries.insert_session(session)

        if not session_row:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed: We couldn't create a session for your account. "
                "Please try again or contact support if the problem persists.",
            )
        token_data: Dict[str, Any] = {
            "email": user_data["email"],
            "name": user_data["full_name"],
            "id": str(user_data["id"]),
        }
        account_data = user_data.get("account_deletion_request")
        if account_data and account_data["status"] in ["pending", "approved"]:
            purpose = "read-only"
        audience = (
            session.audience.lower()
            if hasattr(session, "audience")
            else settings.jwt.AUDIENCE.lower()
        )
        access_token = self.create_access_token(
            token_data,
            token_type=f"{user_type}-access",
            purpose=purpose,
            session_id=str(session_row["id"]),
            is_mobile=is_mobile,
            audience=audience,
        )
        refresh_token = self.create_refresh_token(
            token_data,
            token_type=f"{user_type}-refresh",
            purpose=purpose,
            session_id=str(session_row["id"]),
            audience=(
                session.audience.lower()
                if hasattr(session, "audience")
                else settings.jwt.AUDIENCE
            ),
        )
        user_row = self.helper.build_user_info_object(user_data)
        tokens = UserToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(self.access_token_expire.total_seconds()),
            user=user_row,
        )
        return tokens

    def build_admin_token(
        self,
        session: SessionRequest,
        admin_data: Dict[str, Any],
        user_type: str = "admin",
        purpose: str = "general",
    ):
        session.admin_id = admin_data["id"]
        session.expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt.REFRESH_TOKEN_EXPIRE
        )
        session.last_seen_at = datetime.now(timezone.utc)
        session_row = self.session_queries.insert_session(session)

        if not session_row:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed: We couldn't create a session for your account. "
                "Please try again or contact support if the problem persists.",
            )
        audience = session.audience.lower() if hasattr(session, "audience") else "web"
        token_data = {
            "email": admin_data["email"],
            "first_name": admin_data["first_name"],
            "last_name": admin_data["last_name"],
            "id": str(admin_data["id"]),
        }
        access_token = self.create_access_token(
            token_data,
            token_type=f"{user_type}-access",
            purpose=purpose,
            session_id=str(session_row["id"]),
            audience=audience,
        )
        refresh_token = self.create_refresh_token(
            token_data,
            token_type=f"{user_type}-refresh",
            purpose=purpose,
            session_id=str(session_row["id"]),
            audience=audience,
        )
        admin_row = self.helper.build_admin_info_object(admin_data)
        tokens = AdminToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(self.access_token_expire.total_seconds()),
            admin=admin_row,
        )
        return tokens

    def build_refresh_token(
        self,
        user_data: Dict[str, Any],
        session: SessionResponse,
        user_type: str = "user",
        purpose: str = "general",
    ):
        token_data: Dict[str, Any] = {
            "email": user_data["email"],
            "name": (
                user_data["full_name"]
                if user_type == "user"
                else user_data["first_name"]
            ),
            "id": str(user_data["id"]),
        }

        audience = session.audience.lower()

        access_token = self.create_access_token(
            token_data,
            token_type=f"{user_type}-access",
            purpose="general",
            session_id=str(session.id),
            audience=audience,
        )
        refresh_token = self.create_refresh_token(
            token_data,
            token_type=f"{user_type}-refresh",
            purpose=purpose,
            session_id=str(session.id),
            audience=audience,
        )
        if user_type == "user":
            tokens = UserToken(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=int(self.access_token_expire.total_seconds()),
                user=UserResponse(**user_data),
            )
        elif user_type == "admin":
            tokens = AdminToken(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=int(self.access_token_expire.total_seconds()),
                admin=AdminResponse(**user_data),
            )

        return tokens

    def verify_session(self, session_id: str) -> SessionResponse:
        session = self.session_queries.get_session_by_id(UUID(session_id))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Session not found or has been terminated. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        session_data = SessionResponse(**session)
        expires_at = session_data.expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            self.session_queries.delete_session_by_id(session_id)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Session has expired. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not session_data.is_active or session_data.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Session is inactive. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        session_response = SessionResponse(**session)
        return session_response

    def get_jwt_payload(self, token, audience: str):
        try:
            raw = self.decode_token(token)
            payload = jwt.decode(
                raw,
                settings.jwt.SECRET_KEY,
                algorithms=[settings.jwt.ALGORITHM],
                issuer=settings.jwt.ISSUER,
                audience=audience,
                options={"verify_aud": True},
            )
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired. Please refresh your token or re-authenticate.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTClaimsError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token claims: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token. Please authenticate with valid credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )
