from fastapi import Request
from sqlalchemy.orm import Session

from services.user_service.user_login import (
    UserLoginService
)


class UserLoginController:

    def __init__(self, db: Session):

        self.service = UserLoginService(db)

    def login(
        self,
        account_number: str,
        mpin: str,
        device_id: str,
        device_name: str | None,
        user_agent: str | None,
        ip_address: str | None,
        latitude: float | None,
        longitude: float | None,
        city: str | None,
        country: str | None
    ):

        return self.service.login(
            account_number=account_number,
            mpin=mpin,
            device_id=device_id,
            device_name=device_name,
            user_agent=user_agent,
            ip_address=ip_address,
            latitude=latitude,
            longitude=longitude,
            city=city,
            country=country
        )

    def verify_login_otp(
        self,
        login_otp_id: int,
        otp: str,
        device_id: str,
        device_name: str | None,
        user_agent: str | None,
        ip_address: str | None,
        latitude: float | None,
        longitude: float | None,
        city: str | None,
        country: str | None
    ):

        return self.service.verify_login_otp(
            login_otp_id=login_otp_id,
            otp=otp,
            device_id=device_id,
            device_name=device_name,
            user_agent=user_agent,
            ip_address=ip_address,
            latitude=latitude,
            longitude=longitude,
            city=city,
            country=country
        )