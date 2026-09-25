from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from storage.mysql.models.bank_customer import BankCustomer
from storage.mysql.models.customer_credential import CustomerCredential
from storage.mysql.models.login_attempt import LoginAttempt
from storage.mysql.models.login_otp_verification import LoginOtpVerification
from storage.mysql.models.customer_session import CustomerSession


class UserLoginRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_customer_by_account_number(
        self,
        account_number: str
    ):
        statement = select(BankCustomer).where(
            BankCustomer.account_number == account_number
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def get_customer_by_id(
        self,
        customer_id: int
    ):
        statement = select(BankCustomer).where(
            BankCustomer.customer_id == customer_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def get_credentials_by_customer_id(
        self,
        customer_id: int
    ):
        statement = select(CustomerCredential).where(
            CustomerCredential.customer_id == customer_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def increment_mpin_failed_attempts(
        self,
        credential
    ):
        credential.mpin_failed_attempts += 1

        return credential

    def reset_mpin_failed_attempts(
        self,
        credential
    ):
        credential.mpin_failed_attempts = 0
        credential.mpin_locked_until = None

        return credential

    def lock_mpin(
        self,
        credential,
        locked_until: datetime
    ):
        credential.mpin_locked_until = locked_until
        credential.credential_status = "LOCKED"

        return credential

    def unlock_mpin(
        self,
        credential
    ):
        credential.mpin_failed_attempts = 0
        credential.mpin_locked_until = None
        credential.credential_status = "ACTIVE"

        return credential

    def create_login_attempt(
        self,
        customer_id: int | None,
        ip_address: str | None,
        device_id: str | None,
        user_agent: str | None,
        attempt_status: str,
        failure_reason: str | None = None
    ):
        attempt = LoginAttempt(
            customer_id=customer_id,
            ip_address=ip_address,
            device_id=device_id,
            user_agent=user_agent,
            attempt_status=attempt_status,
            failure_reason=failure_reason
        )

        self.db.add(attempt)
        self.db.flush()

        return attempt

    def create_login_otp(
        self,
        customer_id: int,
        otp_hash: str,
        expires_at: datetime
    ):
        login_otp = LoginOtpVerification(
            customer_id=customer_id,
            otp_hash=otp_hash,
            expires_at=expires_at,
            attempt_count=0,
            verification_status="PENDING"
        )

        self.db.add(login_otp)
        self.db.flush()

        return login_otp

    def get_login_otp(
        self,
        login_otp_id: int
    ):
        statement = select(
            LoginOtpVerification
        ).where(
            LoginOtpVerification.login_otp_id == login_otp_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def get_pending_login_otp(
        self,
        customer_id: int
    ):
        statement = select(
            LoginOtpVerification
        ).where(
            LoginOtpVerification.customer_id == customer_id,
            LoginOtpVerification.verification_status == "PENDING"
        ).order_by(
            LoginOtpVerification.created_at.desc()
        )

        return self.db.execute(
            statement
        ).scalars().first()

    def increment_login_otp_attempt(
        self,
        login_otp
    ):
        login_otp.attempt_count += 1

        return login_otp

    def mark_login_otp_verified(
        self,
        login_otp,
        verified_at: datetime
    ):
        login_otp.verified_at = verified_at
        login_otp.verification_status = "VERIFIED"

        return login_otp

    def mark_login_otp_expired(
        self,
        login_otp
    ):
        login_otp.verification_status = "EXPIRED"

        return login_otp

    def mark_login_otp_failed(
        self,
        login_otp
    ):
        login_otp.verification_status = "FAILED"

        return login_otp

    def cancel_pending_login_otps(
        self,
        customer_id: int
    ):
        statement = (
            update(LoginOtpVerification)
            .where(
                LoginOtpVerification.customer_id == customer_id,
                LoginOtpVerification.verification_status == "PENDING"
            )
            .values(
                verification_status="CANCELLED"
            )
        )

        result = self.db.execute(statement)

        return result.rowcount

    def get_active_sessions(
        self,
        customer_id: int
    ):
        statement = select(
            CustomerSession
        ).where(
            CustomerSession.customer_id == customer_id,
            CustomerSession.session_status == "ACTIVE"
        ).order_by(
            CustomerSession.login_at.desc()
        )

        return self.db.execute(
            statement
        ).scalars().all()

    def get_active_session_by_device(
        self,
        customer_id: int,
        device_id: str
    ):
        statement = select(
            CustomerSession
        ).where(
            CustomerSession.customer_id == customer_id,
            CustomerSession.device_id == device_id,
            CustomerSession.session_status == "ACTIVE"
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def create_customer_session(
        self,
        customer_id: int,
        session_token_hash: str,
        device_id: str | None,
        device_name: str | None,
        ip_address: str | None,
        user_agent: str | None,
        login_latitude: float | None,
        login_longitude: float | None,
        login_city: str | None,
        login_country: str | None,
        login_at: datetime,
        last_activity_at: datetime
    ):
        session = CustomerSession(
            customer_id=customer_id,
            session_token_hash=session_token_hash,
            device_id=device_id,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent,
            login_latitude=login_latitude,
            login_longitude=login_longitude,
            login_city=login_city,
            login_country=login_country,
            login_at=login_at,
            last_activity_at=last_activity_at,
            session_status="ACTIVE"
        )

        self.db.add(session)
        self.db.flush()

        return session

    def get_session_by_id(
        self,
        session_id: int
    ):
        statement = select(
            CustomerSession
        ).where(
            CustomerSession.session_id == session_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def get_session_by_token_hash(
        self,
        session_token_hash: str
    ):
        statement = select(
            CustomerSession
        ).where(
            CustomerSession.session_token_hash == session_token_hash
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def update_session_activity(
        self,
        session,
        last_activity_at: datetime
    ):
        session.last_activity_at = last_activity_at

        return session

    def end_session(
        self,
        session,
        logout_at: datetime
    ):
        session.logout_at = logout_at
        session.session_status = "ENDED"

        return session

    def terminate_session(
        self,
        session,
        logout_at: datetime,
        termination_reason: str
    ):
        session.logout_at = logout_at
        session.session_status = "TERMINATED"
        session.termination_reason = termination_reason

        return session

    def expire_session(
        self,
        session,
        logout_at: datetime
    ):
        session.logout_at = logout_at
        session.session_status = "EXPIRED"

        return session

    def end_all_active_sessions(
        self,
        customer_id: int,
        logout_at: datetime,
        termination_reason: str
    ):
        statement = (
            update(CustomerSession)
            .where(
                CustomerSession.customer_id == customer_id,
                CustomerSession.session_status == "ACTIVE"
            )
            .values(
                session_status="TERMINATED",
                logout_at=logout_at,
                termination_reason=termination_reason
            )
        )

        result = self.db.execute(statement)

        return result.rowcount