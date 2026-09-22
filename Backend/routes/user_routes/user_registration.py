from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from storage.mysql.connection import get_db

from controllers.user_controller.user_registration import (
    UserRegistrationController
)

from schemas.user_schema.user_registration import (
    AccountVerificationRequest,
    AccountVerificationResponse,
    PhoneVerificationRequest,
    PhoneVerificationResponse,
    MpinSetupRequest,
    MpinSetupResponse,
    ResendOtpRequest,
    ResendOtpResponse
)


router = APIRouter(
    prefix="/api/user/registration",
    tags=["User Registration"]
)


@router.post(
    "/verify-account",
    response_model=AccountVerificationResponse
)
def verify_account(
    request: AccountVerificationRequest,
    db: Session = Depends(get_db)
):

    controller = UserRegistrationController(db)

    return controller.verify_account(
        account_number=request.account_number,
        mobile_number=request.mobile_number,
        first_name=request.first_name,
        last_name=request.last_name,
        date_of_birth=request.date_of_birth
    )


@router.post(
    "/verify-phone",
    response_model=PhoneVerificationResponse
)
def verify_phone(
    request: PhoneVerificationRequest,
    db: Session = Depends(get_db)
):

    controller = UserRegistrationController(db)

    return controller.verify_phone(
        registration_id=request.registration_id,
        otp=request.otp
    )


@router.post(
    "/resend-otp",
    response_model=ResendOtpResponse
)
def resend_otp(
    request: ResendOtpRequest,
    db: Session = Depends(get_db)
):

    controller = UserRegistrationController(db)

    return controller.resend_otp(
        registration_id=request.registration_id
    )


@router.post(
    "/setup-mpin",
    response_model=MpinSetupResponse
)
def setup_mpin(
    request: MpinSetupRequest,
    db: Session = Depends(get_db)
):

    controller = UserRegistrationController(db)

    return controller.setup_mpin(
        registration_id=request.registration_id,
        mpin=request.mpin
    )