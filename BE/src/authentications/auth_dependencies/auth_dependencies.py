from typing import Any


from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer


from src.authentication.auth_dependencies.token import AuthToken
from src.helpers.build_session import SessionHelper
from src.helpers.common_models import RequestData
from src.sessions.models import SessionRequest


oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth")


def get_session_data(
    request: Request,
) -> SessionRequest:
    session_helper = SessionHelper()
    session_data = session_helper.get_session_data(request)
    return session_data


class CurrentUser:
    def __init__(
        self,
        user_type: str = "user",
        is_password_reset: bool = False,
        is_refresh: bool = False,
        two_factor: bool = False,
        is_new_password: bool = False,
        is_read_only: bool = False,
    ):
        self.token = AuthToken()
        self.user_type = user_type
        self.is_password_reset = is_password_reset
        self.is_refresh = is_refresh
        self.two_factor = two_factor
        self.is_new_password = is_new_password
        self.is_read_only = is_read_only
        self.session_helper = SessionHelper()

    async def __call__(
        self,
        request: Request,
        token: str = Depends(oauth2_schema),
        session: SessionRequest = Depends(get_session_data),
    ) -> Any:
        # Verify token based on user type
        if self.user_type == "admin":
            token_data = self.token.verify_admin_token(
                token,
                self.is_refresh,
                is_password_reset=self.is_password_reset,
                two_factor=self.two_factor,
                is_new_password=self.is_new_password,
                audience=session.audience.lower(),
            )
            session.admin_id = token_data.admin_id

        elif self.user_type == "user":
            token_data = self.token.verify_user_token(
                token,
                self.is_refresh,
                is_password_reset=self.is_password_reset,
                two_factor=self.two_factor,
                is_read_only=self.is_read_only,
                audience=session.audience.lower(),
            )
            session.user_id = token_data.user_id

        else:
            payload = self.token.get_jwt_payload(token, session.audience.lower())
            if "user" in payload.get("type", ""):
                token_data = self.token.verify_user_token(
                    token,
                    self.is_refresh,
                    is_password_reset=self.is_password_reset,
                    two_factor=self.two_factor,
                    is_read_only=self.is_read_only,
                    audience=session.audience.lower(),
                )
                session.user_id = token_data.user_id
            else:
                token_data = self.token.verify_admin_token(
                    token,
                    self.is_refresh,
                    is_password_reset=self.is_password_reset,
                    two_factor=self.two_factor,
                    is_new_password=self.is_new_password,
                    audience=session.audience.lower(),
                )
                session.admin_id = token_data.admin_id

        request_data = RequestData(token_data=token_data, session=session)
        return request_data
