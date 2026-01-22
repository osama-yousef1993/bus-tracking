import re
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID


from pydantic import BaseModel, Field, field_validator


from src.admins.models import AdminResponse
from src.helpers.patterns import (
    email_error_message,
    email_pattern,
    name_pattern,
    password_error_message,
    password_pattern,
    phone_error_message,
    phone_pattern,
)
from src.users.models import UserResponse


class UserToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class UserTokenData(BaseModel):
    user_id: UUID
    session_id: Optional[str] = None
    user_setting_id: UUID
    full_name: str
    email: str
    phone: str
    exp: datetime
    type: Optional[str] | None = None
    pur: Optional[str] | None = None


class Register(BaseModel):
    full_name: str = Field(pattern=name_pattern, max_length=50, min_length=1)
    account_type: str
    email: str = Field(max_length=50, min_length=9)
    phone: str = Field(max_length=50, min_length=10)
    password: str = Field(max_length=1000, min_length=8)
    country: str
    timezone: str
    language: Optional[str] | None = None

    @field_validator("phone")
    def validate_phone(cls, v: str):
        if not re.fullmatch(phone_pattern, v):
            raise ValueError(phone_error_message)
        return v

    @field_validator("password")
    def validate_password(cls, v: str):
        if not re.fullmatch(password_pattern, v):
            raise ValueError(password_error_message)
        return v

    @field_validator("email")
    def validate_email(cls, v: str):
        if not re.fullmatch(email_pattern, v):
            raise ValueError(email_error_message)
        return v.lower()


class RegisterResponse(BaseModel):
    message: str
    user_id: str
    email: str
    status: str


class AdminToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    admin: AdminResponse


class AdminTokenData(BaseModel):
    admin_id: UUID
    session_id: Optional[str] = None
    email: Optional[str] = None
    exp: Optional[datetime] = None
    type: Optional[str] = None
    pur: Optional[str] = None


class ResetPassword(BaseModel):
    email: str = Field(max_length=50, min_length=4)
    otp_code: str
    password: str = Field(max_length=1000, min_length=8)

    @field_validator("password")
    def validate_password(cls, v: str):
        if not re.fullmatch(password_pattern, v):
            raise ValueError(password_error_message)
        return v

    @field_validator("email")
    def validate_email(cls, v: str):
        if not re.fullmatch(email_pattern, v):
            raise ValueError(email_error_message)
        return v.lower()


class LoginRequest(BaseModel):
    email: str = Field(max_length=50, min_length=1)
    password: str = Field(max_length=1000, min_length=8)

    @field_validator("password")
    def validate_password(cls, v: str):
        if not re.fullmatch(password_pattern, v):
            raise ValueError(password_error_message)
        return v

    @field_validator("email")
    def validate_email(cls, v: str):
        if not re.fullmatch(email_pattern, v):
            raise ValueError(email_error_message)
        return v.lower()


class EmailRequestSchema(BaseModel):
    to_email: str
    subject: str
    html_content: str

    @field_validator("to_email")
    def validate_email(cls, v: str):
        if not re.fullmatch(email_pattern, v):
            raise ValueError(email_error_message)
        return v.lower()


class RefreshToken(BaseModel):
    refresh_token: str


class ActivationRequest(BaseModel):
    token: str


class OTPRequest(BaseModel):
    email: str
    otp_code: str

    @field_validator("email")
    def validate_email(cls, v: str):
        if not re.fullmatch(email_pattern, v):
            raise ValueError(email_error_message)
        return v.lower()


# Tokens
class JwtToken(BaseModel):
    audience: str
    issuer: str
    device_id: str
    ip_address: str


class ActiveUsersResponse(BaseModel):
    active_users: int


class TwoFactorSetUp(BaseModel):
    """
    Two-factor authentication setup model.


    Attributes:
        two_fa_type: The method used for 2FA.
                     Allowed values: "sms", "authenticator".
    """

    two_fa_type: Literal["sms", "authenticator"]


class Verify2FARequest(BaseModel):
    otp_code: str = Field(max_length=6, min_length=6)


class GoogleSignupRequired(BaseModel):
    google_signup_token: str
    phone: str
    country: str
    full_name: str
    tz_data: str


class CallbackRespons(BaseModel):
    google_signup_token: str
    full_name: str


class GoogleLoginContent(BaseModel):
    redirect_uri: str
