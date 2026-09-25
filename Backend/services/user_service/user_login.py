import os
import secrets
import hashlib
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from jose import jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from repositories.user_repository.user_login import (
    UserLoginRepository
)


class UserLoginService:

    def __init__(self, db: Session):

        self.db = db
        self.repository = UserLoginRepository(db)

        self.password_hash = PasswordHash.recommended()

        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY")
        self.jwt_algorithm = os.getenv(
            "JWT_ALGORITHM",
            "HS256"
        )

        self.jwt_expire_minutes = int(
            os.getenv(
                "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
                "60"
            )
        )

        self.login_otp_expire_minutes = int(
            os.getenv(
                "LOGIN_OTP_EXPIRE_MINUTES",
                "10"
            )
        )

        self.max_mpin_attempts = int(
            os.getenv(
                "LOGIN_MAX_MPIN_ATTEMPTS",
                "5"
            )
        )

        self.max_otp_attempts = int(
            os.getenv(
                "LOGIN_MAX_OTP_ATTEMPTS",
                "5"
            )
        )

        self.pushover_api_token = os.getenv(
            "PUSHOVER_API_TOKEN"
        )

        self.pushover_user_key = os.getenv(
            "PUSHOVER_USER_KEY"
        )

        self.mail_host = os.getenv(
            "MAIL_HOST",
            "smtp.gmail.com"
        )

        self.mail_port = int(
            os.getenv(
                "MAIL_PORT",
                "587"
            )
        )

        self.mail_username = os.getenv(
            "MAIL_USERNAME"
        )

        self.mail_password = os.getenv(
            "MAIL_PASSWORD"
        )

        self.mail_from_email = os.getenv(
            "MAIL_FROM_EMAIL"
        )

        self.mail_from_name = os.getenv(
            "MAIL_FROM_NAME",
            "AegisLend AI"
        )

        if not self.jwt_secret_key:
            raise RuntimeError(
                "JWT_SECRET_KEY is not configured."
            )

        if not self.pushover_api_token:
            raise RuntimeError(
                "PUSHOVER_API_TOKEN is not configured."
            )

        if not self.pushover_user_key:
            raise RuntimeError(
                "PUSHOVER_USER_KEY is not configured."
            )

        if not self.mail_username:
            raise RuntimeError(
                "MAIL_USERNAME is not configured."
            )

        if not self.mail_password:
            raise RuntimeError(
                "MAIL_PASSWORD is not configured."
            )

        if not self.mail_from_email:
            raise RuntimeError(
                "MAIL_FROM_EMAIL is not configured."
            )

    def generate_otp(self):

        return str(
            secrets.randbelow(900000) + 100000
        )

    def hash_token(self, token: str):

        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

    def create_access_token(
        self,
        customer_id: int,
        session_id: int
    ):

        now = datetime.now(timezone.utc)

        expires_at = (
            now +
            timedelta(
                minutes=self.jwt_expire_minutes
            )
        )

        payload = {
            "sub": str(customer_id),
            "session_id": session_id,
            "jti": secrets.token_hex(16),
            "iat": now,
            "exp": expires_at
        }

        token = jwt.encode(
            payload,
            self.jwt_secret_key,
            algorithm=self.jwt_algorithm
        )

        return token, expires_at

    def send_login_otp(
        self,
        otp: str
    ):

        import httpx

        message = (
            f"Your AegisLend AI login OTP is {otp}.\n\n"
            f"Do not share this OTP with anyone.\n"
            f"Valid for {self.login_otp_expire_minutes} minutes."
        )

        payload = {
            "token": self.pushover_api_token,
            "user": self.pushover_user_key,
            "title": "AegisLend AI Login OTP",
            "message": message
        }

        response = httpx.post(
            "https://api.pushover.net/1/messages.json",
            data=payload,
            timeout=10
        )

        response_data = response.json()

        if (
            response.status_code != 200
            or response_data.get("status") != 1
        ):
            raise RuntimeError(
                "Unable to send login OTP."
            )

        return True

    def send_login_notification(
        self,
        customer,
        ip_address: str | None,
        device_name: str | None,
        city: str | None,
        country: str | None,
        login_time: datetime
    ):

        if not customer.email:
            return False

        message = EmailMessage()

        message["Subject"] = (
            "AegisLend AI - New Login Detected"
        )

        message["From"] = (
            f"{self.mail_from_name} "
            f"<{self.mail_from_email}>"
        )

        message["To"] = customer.email

        formatted_time = login_time.strftime(
            "%d %B %Y, %I:%M %p"
        )

        location = "Location unavailable"

        if city and country:
            location = f"{city}, {country}"
        elif country:
            location = country

        device = (
            device_name
            if device_name
            else "Unknown device"
        )

        body = (
            f"Hello {customer.first_name},\n\n"
            f"A new login to your AegisLend AI account "
            f"was detected.\n\n"
            f"Login details:\n"
            f"Date and time: {formatted_time}\n"
            f"Location: {location}\n"
            f"IP address: {ip_address or 'Unavailable'}\n"
            f"Device: {device}\n\n"
            f"If this was you, no action is required.\n\n"
            f"If you do not recognize this login, "
            f"secure your account immediately and contact "
            f"AegisLend AI support.\n\n"
            f"Regards,\n"
            f"AegisLend AI Security Team"
        )

        message.set_content(body)

        with smtplib.SMTP(
            self.mail_host,
            self.mail_port,
            timeout=15
        ) as smtp:

            smtp.starttls()

            smtp.login(
                self.mail_username,
                self.mail_password
            )

            smtp.send_message(message)

        return True

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

        try:

            if latitude is None or longitude is None:

                return {
                    "success": False,
                    "message": (
                        "Location permission is required "
                        "to authenticate securely."
                    ),
                    "login_otp_id": None,
                    "next_step": "LOCATION_REQUIRED"
                }

            customer = (
                self.repository
                .get_customer_by_account_number(
                    account_number
                )
            )

            if not customer:

                self.repository.create_login_attempt(
                    customer_id=None,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status="FAILED",
                    failure_reason="ACCOUNT_NOT_FOUND"
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": (
                        "Invalid account number or MPIN."
                    ),
                    "login_otp_id": None,
                    "next_step": "LOGIN_FAILED"
                }

            if customer.account_status != "ACTIVE":

                self.repository.create_login_attempt(
                    customer_id=customer.customer_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status="BLOCKED",
                    failure_reason=(
                        f"ACCOUNT_{customer.account_status}"
                    )
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": (
                        "This account is not available "
                        "for login."
                    ),
                    "login_otp_id": None,
                    "next_step": "LOGIN_BLOCKED"
                }

            credential = (
                self.repository
                .get_credentials_by_customer_id(
                    customer.customer_id
                )
            )

            if not credential:

                self.repository.create_login_attempt(
                    customer_id=customer.customer_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status="FAILED",
                    failure_reason="CREDENTIAL_NOT_FOUND"
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": (
                        "Account authentication is "
                        "not available."
                    ),
                    "login_otp_id": None,
                    "next_step": "LOGIN_FAILED"
                }

            now = datetime.utcnow()

            if (
                credential.mpin_locked_until
                and credential.mpin_locked_until > now
            ):

                self.repository.create_login_attempt(
                    customer_id=customer.customer_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status="BLOCKED",
                    failure_reason="MPIN_LOCKED"
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": (
                        "MPIN is temporarily locked. "
                        "Please try again later."
                    ),
                    "login_otp_id": None,
                    "next_step": "MPIN_LOCKED"
                }

            if credential.credential_status == "LOCKED":

                if (
                    not credential.mpin_locked_until
                    or credential.mpin_locked_until <= now
                ):

                    self.repository.unlock_mpin(
                        credential
                    )

                    self.db.flush()

                else:

                    self.repository.create_login_attempt(
                        customer_id=customer.customer_id,
                        ip_address=ip_address,
                        device_id=device_id,
                        user_agent=user_agent,
                        attempt_status="BLOCKED",
                        failure_reason="CREDENTIAL_LOCKED"
                    )

                    self.db.commit()

                    return {
                        "success": False,
                        "message": (
                            "MPIN is currently locked."
                        ),
                        "login_otp_id": None,
                        "next_step": "MPIN_LOCKED"
                    }

            if credential.credential_status != "ACTIVE":

                self.repository.create_login_attempt(
                    customer_id=customer.customer_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status="BLOCKED",
                    failure_reason="CREDENTIAL_DISABLED"
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": (
                        "Your login credential is disabled."
                    ),
                    "login_otp_id": None,
                    "next_step": "LOGIN_BLOCKED"
                }

            if not self.password_hash.verify(
                mpin,
                credential.mpin_hash
            ):

                self.repository.increment_mpin_failed_attempts(
                    credential
                )

                failure_count = (
                    credential.mpin_failed_attempts
                )

                if (
                    failure_count
                    >= self.max_mpin_attempts
                ):

                    locked_until = (
                        now +
                        timedelta(minutes=15)
                    )

                    self.repository.lock_mpin(
                        credential,
                        locked_until
                    )

                    failure_reason = (
                        "MPIN_ATTEMPTS_EXCEEDED"
                    )

                    attempt_status = "BLOCKED"

                    message = (
                        "Too many failed MPIN attempts. "
                        "Your MPIN has been temporarily locked."
                    )

                    next_step = "MPIN_LOCKED"

                else:

                    failure_reason = "INVALID_MPIN"
                    attempt_status = "FAILED"

                    remaining = (
                        self.max_mpin_attempts
                        - failure_count
                    )

                    message = (
                        "Invalid account number or MPIN."
                    )

                    next_step = "LOGIN_FAILED"

                self.repository.create_login_attempt(
                    customer_id=customer.customer_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status=attempt_status,
                    failure_reason=failure_reason
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": message,
                    "login_otp_id": None,
                    "next_step": next_step
                }

            self.repository.reset_mpin_failed_attempts(
                credential
            )

            self.repository.cancel_pending_login_otps(
                customer.customer_id
            )

            otp = self.generate_otp()

            otp_hash = self.password_hash.hash(
                otp
            )

            otp_expires_at = (
                now +
                timedelta(
                    minutes=self.login_otp_expire_minutes
                )
            )

            login_otp = (
                self.repository.create_login_otp(
                    customer_id=customer.customer_id,
                    otp_hash=otp_hash,
                    expires_at=otp_expires_at
                )
            )

            self.repository.create_login_attempt(
                customer_id=customer.customer_id,
                ip_address=ip_address,
                device_id=device_id,
                user_agent=user_agent,
                attempt_status="OTP_REQUIRED",
                failure_reason=None
            )

            self.send_login_otp(otp)

            self.db.commit()

            return {
                "success": True,
                "message": (
                    "MPIN verified. Login OTP sent "
                    "successfully."
                ),
                "login_otp_id": login_otp.login_otp_id,
                "next_step": "OTP_REQUIRED"
            }

        except Exception as e:

            self.db.rollback()

            return {
                "success": False,
                "message": str(e),
                "login_otp_id": None,
                "next_step": "LOGIN_FAILED"
            }

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

        try:

            if latitude is None or longitude is None:

                return {
                    "success": False,
                    "message": (
                        "Location permission is required "
                        "to complete login."
                    ),
                    "next_step": "LOCATION_REQUIRED",
                    "access_token": None,
                    "token_type": None,
                    "expires_in": None
                }

            login_otp = (
                self.repository
                .get_login_otp(login_otp_id)
            )

            if not login_otp:

                return {
                    "success": False,
                    "message": "Invalid login OTP request.",
                    "next_step": "LOGIN_FAILED",
                    "access_token": None,
                    "token_type": None,
                    "expires_in": None
                }

            customer = (
                self.repository
                .get_customer_by_id(
                    login_otp.customer_id
                )
            )

            if not customer:

                return {
                    "success": False,
                    "message": "Customer not found.",
                    "next_step": "LOGIN_FAILED",
                    "access_token": None,
                    "token_type": None,
                    "expires_in": None
                }

            now = datetime.utcnow()

            if (
                login_otp.verification_status
                != "PENDING"
            ):

                return {
                    "success": False,
                    "message": (
                        "This login OTP is no longer valid."
                    ),
                    "next_step": "OTP_INVALID",
                    "access_token": None,
                    "token_type": None,
                    "expires_in": None
                }

            if now >= login_otp.expires_at:

                self.repository.mark_login_otp_expired(
                    login_otp
                )

                self.repository.create_login_attempt(
                    customer_id=customer.customer_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status="FAILED",
                    failure_reason="LOGIN_OTP_EXPIRED"
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": (
                        "Login OTP has expired."
                    ),
                    "next_step": "OTP_EXPIRED",
                    "access_token": None,
                    "token_type": None,
                    "expires_in": None
                }

            if (
                login_otp.attempt_count
                >= self.max_otp_attempts
            ):

                self.repository.mark_login_otp_failed(
                    login_otp
                )

                self.repository.create_login_attempt(
                    customer_id=customer.customer_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status="BLOCKED",
                    failure_reason="LOGIN_OTP_ATTEMPTS_EXCEEDED"
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": (
                        "Too many incorrect OTP attempts."
                    ),
                    "next_step": "OTP_BLOCKED",
                    "access_token": None,
                    "token_type": None,
                    "expires_in": None
                }

            if not self.password_hash.verify(
                otp,
                login_otp.otp_hash
            ):

                self.repository.increment_login_otp_attempt(
                    login_otp
                )

                if (
                    login_otp.attempt_count
                    >= self.max_otp_attempts
                ):

                    self.repository.mark_login_otp_failed(
                        login_otp
                    )

                    attempt_status = "BLOCKED"
                    failure_reason = (
                        "LOGIN_OTP_ATTEMPTS_EXCEEDED"
                    )

                    message = (
                        "Too many incorrect OTP attempts."
                    )

                    next_step = "OTP_BLOCKED"

                else:

                    attempt_status = "FAILED"
                    failure_reason = "INVALID_LOGIN_OTP"

                    remaining = (
                        self.max_otp_attempts
                        - login_otp.attempt_count
                    )

                    message = (
                        "Invalid OTP."
                    )

                    next_step = "OTP_INVALID"

                self.repository.create_login_attempt(
                    customer_id=customer.customer_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    user_agent=user_agent,
                    attempt_status=attempt_status,
                    failure_reason=failure_reason
                )

                self.db.commit()

                return {
                    "success": False,
                    "message": message,
                    "next_step": next_step,
                    "access_token": None,
                    "token_type": None,
                    "expires_in": None
                }

            self.repository.mark_login_otp_verified(
                login_otp,
                now
            )

            active_sessions = (
                self.repository
                .get_active_sessions(
                    customer.customer_id
                )
            )

            same_device_session = (
                self.repository
                .get_active_session_by_device(
                    customer.customer_id,
                    device_id
                )
            )

            token_placeholder = secrets.token_urlsafe(
                32
            )

            token_placeholder_hash = (
                self.hash_token(
                    token_placeholder
                )
            )

            session = (
                self.repository.create_customer_session(
                    customer_id=customer.customer_id,
                    session_token_hash=token_placeholder_hash,
                    device_id=device_id,
                    device_name=device_name,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    login_latitude=latitude,
                    login_longitude=longitude,
                    login_city=city,
                    login_country=country,
                    login_at=now,
                    last_activity_at=now
                )
            )

            access_token, expires_at = (
                self.create_access_token(
                    customer_id=customer.customer_id,
                    session_id=session.session_id
                )
            )

            real_token_hash = self.hash_token(
                access_token
            )

            session.session_token_hash = (
                real_token_hash
            )

            self.repository.create_login_attempt(
                customer_id=customer.customer_id,
                ip_address=ip_address,
                device_id=device_id,
                user_agent=user_agent,
                attempt_status="SUCCESS",
                failure_reason=None
            )

            self.db.commit()

            try:

                self.send_login_notification(
                    customer=customer,
                    ip_address=ip_address,
                    device_name=device_name,
                    city=city,
                    country=country,
                    login_time=now
                )

            except Exception as email_error:

                print(
                    f"Login notification email failed: "
                    f"{email_error}"
                )

            return {
                "success": True,
                "message": "Login successful.",
                "next_step": "AUTHENTICATED",
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": int(
                    (
                        expires_at -
                        datetime.now(timezone.utc)
                    ).total_seconds()
                )
            }

        except Exception as e:

            self.db.rollback()

            return {
                "success": False,
                "message": str(e),
                "next_step": "LOGIN_FAILED",
                "access_token": None,
                "token_type": None,
                "expires_in": None
            }