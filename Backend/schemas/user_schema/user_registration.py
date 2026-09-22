from datetime import date, datetime

from pydantic import (
    BaseModel,
    Field,
    model_validator
)


class AccountVerificationRequest(BaseModel):

    account_number: str = Field(
        min_length=1,
        max_length=20
    )

    mobile_number: str = Field(
        min_length=10,
        max_length=15
    )

    first_name: str = Field(
        min_length=1,
        max_length=50
    )

    last_name: str = Field(
        min_length=1,
        max_length=50
    )

    date_of_birth: date


class AccountVerificationResponse(BaseModel):

    success: bool

    message: str

    registration_id: int | None = None

    next_step: str | None = None

    registration_expires_at: datetime | None = None


class PhoneVerificationRequest(BaseModel):

    registration_id: int

    otp: str = Field(
        min_length=6,
        max_length=6
    )

    @model_validator(mode="after")
    def validate_otp(self):

        if not self.otp.isdigit():
            raise ValueError(
                "OTP must contain only digits."
            )

        return self


class PhoneVerificationResponse(BaseModel):

    success: bool

    message: str

    registration_id: int | None = None

    next_step: str | None = None


class ResendOtpRequest(BaseModel):

    registration_id: int


class ResendOtpResponse(BaseModel):

    success: bool

    message: str

    registration_id: int | None = None

    next_step: str | None = None


class MpinSetupRequest(BaseModel):

    registration_id: int

    mpin: str = Field(
        min_length=6,
        max_length=6
    )

    confirm_mpin: str = Field(
        min_length=6,
        max_length=6
    )

    @model_validator(mode="after")
    def validate_mpin(self):

        if not self.mpin.isdigit():
            raise ValueError(
                "MPIN must contain only digits."
            )

        if self.mpin != self.confirm_mpin:
            raise ValueError(
                "MPIN and confirm MPIN do not match."
            )

        return self


class MpinSetupResponse(BaseModel):

    success: bool

    message: str

    registration_id: int | None = None

    next_step: str | None = None