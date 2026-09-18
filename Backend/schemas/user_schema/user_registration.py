from datetime import date, datetime

from pydantic import BaseModel, Field


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

    firebase_id_token: str = Field(
        min_length=1
    )


class PhoneVerificationResponse(BaseModel):

    success: bool
    message: str

    registration_id: int | None = None

    next_step: str | None = None