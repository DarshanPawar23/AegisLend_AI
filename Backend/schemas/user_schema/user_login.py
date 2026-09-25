from pydantic import (
    BaseModel,
    Field,
    model_validator
)


class LoginRequest(BaseModel):

    account_number: str = Field(
        min_length=1,
        max_length=20
    )

    mpin: str = Field(
        min_length=6,
        max_length=6
    )

    device_id: str = Field(
        min_length=1,
        max_length=255
    )

    device_name: str | None = Field(
        default=None,
        max_length=150
    )

    user_agent: str | None = Field(
        default=None,
        max_length=500
    )

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180
    )

    city: str | None = Field(
        default=None,
        max_length=100
    )

    country: str | None = Field(
        default=None,
        max_length=100
    )

    @model_validator(mode="after")
    def validate_mpin(self):

        if not self.mpin.isdigit():
            raise ValueError(
                "MPIN must contain only digits."
            )

        return self


class LoginResponse(BaseModel):

    success: bool
    message: str
    login_otp_id: int | None = None
    next_step: str | None = None


class LoginOtpVerificationRequest(BaseModel):
    login_otp_id: int
    otp: str = Field(min_length=6, max_length=6)
    device_id: str = Field(default="WEB_CLIENT", min_length=1, max_length=255)
    device_name: str | None = Field(default=None, max_length=150)
    user_agent: str | None = Field(default=None, max_length=500)
    latitude: float | None = None
    longitude: float | None = None
    city: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)


class LoginOtpVerificationResponse(BaseModel):

    success: bool
    message: str
    next_step: str | None = None
    access_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None


class ResendLoginOtpRequest(BaseModel):

    login_otp_id: int


class ResendLoginOtpResponse(BaseModel):

    success: bool
    message: str
    login_otp_id: int | None = None
    next_step: str | None = None


class LogoutResponse(BaseModel):

    success: bool
    message: str