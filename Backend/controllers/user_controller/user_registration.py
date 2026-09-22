from sqlalchemy.orm import Session

from services.user_service.user_registration import (
    UserRegistrationService
)


class UserRegistrationController:

    def __init__(self, db: Session):

        self.service = UserRegistrationService(db)

    def verify_account(
        self,
        account_number: str,
        mobile_number: str,
        first_name: str,
        last_name: str,
        date_of_birth
    ):

        return self.service.verify_account(
            account_number=account_number,
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )

    def verify_phone(
    self,
    registration_id: int,
    otp: str
    ):

        return self.service.verify_phone(
        registration_id=registration_id,
        otp=otp
        )

    def setup_mpin(
    self,
    registration_id: int,
    mpin: str
    ):

        return self.service.setup_mpin(
            registration_id=registration_id,
            mpin=mpin
        )
