from fastapi import (
    APIRouter,
    Depends,
    Request
)

from sqlalchemy.orm import Session

from storage.mysql.connection import get_db

from controllers.user_controller.user_login import (
    UserLoginController
)

from schemas.user_schema.user_login import (
    LoginRequest,
    LoginResponse,
    LoginOtpVerificationRequest,
    LoginOtpVerificationResponse
)


router = APIRouter(
    prefix="/api/user/login",
    tags=["User Login"]
)


@router.post(
    "",
    response_model=LoginResponse
)
def login(
    request: Request,
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):

    controller = UserLoginController(db)

    ip_address = None

    if request.client:
        ip_address = request.client.host

    user_agent = (
        login_request.user_agent
        or request.headers.get("user-agent")
    )

    return controller.login(
        account_number=login_request.account_number,
        mpin=login_request.mpin,
        device_id=login_request.device_id,
        device_name=login_request.device_name,
        user_agent=user_agent,
        ip_address=ip_address,
        latitude=login_request.latitude,
        longitude=login_request.longitude,
        city=login_request.city,
        country=login_request.country
    )


@router.post(
    "/verify-otp",
    response_model=LoginOtpVerificationResponse
)
def verify_login_otp(
    request: Request,
    otp_request: LoginOtpVerificationRequest,
    db: Session = Depends(get_db)
):
    controller = UserLoginController(db)

    ip_address = None
    if request.client:
        ip_address = request.client.host

    user_agent = (
        otp_request.user_agent
        or request.headers.get("user-agent")
    )

    return controller.verify_login_otp(
        login_otp_id=otp_request.login_otp_id,
        otp=otp_request.otp,
        device_id=otp_request.device_id,
        device_name=otp_request.device_name,
        user_agent=user_agent,
        ip_address=ip_address,
        latitude=otp_request.latitude,
        longitude=otp_request.longitude,
        city=otp_request.city,
        country=otp_request.country
    )