from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from storage.mysql.models.bank_customer import BankCustomer
from storage.mysql.models.user_app_registration import (
    UserAppRegistration
)
from storage.mysql.models.registration_verification import (
    RegistrationVerification
)
from storage.mysql.models.customer_credential import (
    CustomerCredential
)


class UserRegistrationRepository:

    def __init__(self, db: Session):
        self.db = db


    def find_customer_for_registration(
        self,
        account_number: str,
        mobile_number: str,
        first_name: str,
        last_name: str,
        date_of_birth
    ):

        statement = select(BankCustomer).where(
            BankCustomer.account_number == account_number,
            BankCustomer.mobile_number == mobile_number,
            BankCustomer.first_name == first_name,
            BankCustomer.last_name == last_name,
            BankCustomer.date_of_birth == date_of_birth
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def get_registration_by_customer_id(
        self,
        customer_id: int
    ):

        statement = select(
            UserAppRegistration
        ).where(
            UserAppRegistration.customer_id == customer_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def get_registration(
        self,
        registration_id: int
    ):

        statement = select(
            UserAppRegistration
        ).where(
            UserAppRegistration.registration_id
            == registration_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def create_registration(
        self,
        customer_id: int,
        expires_at: datetime
    ):

        registration = UserAppRegistration(
            customer_id=customer_id,
            registration_status="OTP_PENDING",
            account_verified_at=datetime.utcnow(),
            expires_at=expires_at
        )

        self.db.add(registration)
        self.db.flush()

        return registration


    def create_verification(
        self,
        registration_id: int,
        otp_hash: str,
        expires_at: datetime
    ):

        verification = RegistrationVerification(
            registration_id=registration_id,
            verification_type="MOBILE_OTP",
            otp_hash=otp_hash,
            expires_at=expires_at,
            attempt_count=0,
            verification_status="PENDING"
        )

        self.db.add(verification)
        self.db.flush()

        return verification

    def get_pending_otp(
        self,
        registration_id: int
    ):

        statement = select(
            RegistrationVerification
        ).where(
            RegistrationVerification.registration_id
            == registration_id,

            RegistrationVerification.verification_type
            == "MOBILE_OTP",

            RegistrationVerification.verification_status
            == "PENDING"
        ).order_by(
            RegistrationVerification.created_at.desc()
        )

        return self.db.execute(
            statement
        ).scalars().first()

    def increment_otp_attempt(
        self,
        verification: RegistrationVerification
    ):

        verification.attempt_count += 1

        return verification

    def mark_otp_verified(
        self,
        verification: RegistrationVerification,
        verified_at: datetime
    ):

        verification.verified_at = verified_at

        verification.verification_status = "VERIFIED"

        return verification

    def mark_otp_expired(
        self,
        verification: RegistrationVerification
    ):

        verification.verification_status = "EXPIRED"

        return verification

    def mark_otp_failed(
        self,
        verification: RegistrationVerification
    ):

        verification.verification_status = "FAILED"

        return verification


    def delete_expired_registration(
        self,
        registration_id: int
    ):

        self.db.execute(
            delete(
                RegistrationVerification
            ).where(
                RegistrationVerification.registration_id
                == registration_id
            )
        )

        self.db.execute(
            delete(
                UserAppRegistration
            ).where(
                UserAppRegistration.registration_id
                == registration_id
            )
        )

    def delete_expired_registrations(
        self
    ):

        now = datetime.utcnow()

        statement = select(
            UserAppRegistration
        ).where(
            UserAppRegistration.expires_at <= now,
            UserAppRegistration.registration_status
            != "REGISTERED"
        )

        registrations = self.db.execute(
            statement
        ).scalars().all()

        for registration in registrations:

            self.delete_expired_registration(
                registration.registration_id
            )

        return len(registrations)


    def get_customer_by_registration(
        self,
        registration_id: int
    ):

        statement = (
            select(BankCustomer)
            .join(
                UserAppRegistration,
                UserAppRegistration.customer_id
                == BankCustomer.customer_id
            )
            .where(
                UserAppRegistration.registration_id
                == registration_id
            )
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()


    def get_credential_by_customer_id(
        self,
        customer_id: int
    ):

        statement = select(
            CustomerCredential
        ).where(
            CustomerCredential.customer_id
            == customer_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def create_customer_credential(
        self,
        customer_id: int,
        mpin_hash: str,
        created_at: datetime
    ):

        credential = CustomerCredential(
            customer_id=customer_id,
            mpin_hash=mpin_hash,
            mpin_failed_attempts=0,
            mpin_locked_until=None,
            last_mpin_changed_at=created_at,
            credential_status="ACTIVE"
        )

        self.db.add(credential)
        self.db.flush()

        return credential