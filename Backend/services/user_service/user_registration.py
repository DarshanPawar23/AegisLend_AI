import os
import secrets
import httpx

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from pwdlib import PasswordHash

from repositories.user_repository.user_registration import (
    UserRegistrationRepository
)


class UserRegistrationService:

    password_hash = PasswordHash.recommended()

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRegistrationRepository(db)

        self.pushover_api_token = os.getenv(
            "PUSHOVER_API_TOKEN"
        )

        self.pushover_user_key = os.getenv(
            "PUSHOVER_USER_KEY"
        )

        if not self.pushover_api_token:
            raise RuntimeError(
                "PUSHOVER_API_TOKEN is not configured."
            )

        if not self.pushover_user_key:
            raise RuntimeError(
                "PUSHOVER_USER_KEY is not configured."
            )

    def generate_otp(self) -> str:
        return str(
            secrets.randbelow(900000) + 100000
        )

    def send_otp(
        self,
        mobile_number: str,
        otp: str
    ):
        print("\n" + "=" * 50)
        print("AEGISLEND AI OTP DISPATCH")
        print(f"6-Digit OTP   : {otp}")
        print("=" * 50 + "\n")

        message = (
            f"Your AegisLend AI OTP is {otp}.\n\n"
            f"Do not share this OTP with anyone.\n"
            f"Valid for 10 minutes."
        )

        payload = {
            "token": self.pushover_api_token,
            "user": self.pushover_user_key,
            "title": "AegisLend AI OTP",
            "message": message
        }

        try:
            response = httpx.post(
                "https://api.pushover.net/1/messages.json",
                data=payload,
                timeout=10
            )

            try:
                response_data = response.json()
            except ValueError:
                response_data = {}

            print(
                "Pushover Status Code:",
                response.status_code
            )

            print(
                "Pushover Response Data:",
                response_data
            )

        except httpx.RequestError as e:
            print(
                "Pushover Connection Exception:",
                str(e)
            )

            return {
                "success": False,
                "message": (
                    "Unable to connect to Pushover."
                )
            }

        if response.status_code != 200:
            errors = response_data.get(
                "errors",
                ["Pushover rejected the request."]
            )

            return {
                "success": False,
                "message": errors[0]
            }

        if response_data.get("status") != 1:
            return {
                "success": False,
                "message": (
                    "Pushover failed to send "
                    "the notification."
                )
            }

        return {
            "success": True,
            "message": (
                "OTP sent successfully "
                "through Pushover."
            )
        }

    def verify_account(
        self,
        account_number: str,
        mobile_number: str,
        first_name: str,
        last_name: str,
        date_of_birth
    ):
        customer = (
            self.repository.find_customer_for_registration(
                account_number=account_number,
                mobile_number=mobile_number,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth
            )
        )

        if not customer:
            return {
                "success": False,
                "message": (
                    "The provided account details "
                    "could not be verified."
                )
            }

        if customer.account_status != "ACTIVE":
            return {
                "success": False,
                "message": (
                    "The bank account is not active."
                )
            }

        registration = (
            self.repository.get_registration_by_customer_id(
                customer.customer_id
            )
        )

        now = datetime.utcnow()

        if registration:

            if (
                registration.registration_status
                == "REGISTERED"
            ):
                return {
                    "success": False,
                    "message": (
                        "This account is already "
                        "registered."
                    )
                }

            if registration.expires_at <= now:
                self.repository.delete_expired_registration(
                    registration.registration_id
                )

                self.db.commit()

                registration = None

        if not registration:
            registration_expires_at = (
                now + timedelta(hours=24)
            )

            registration = (
                self.repository.create_registration(
                    customer_id=customer.customer_id,
                    expires_at=registration_expires_at
                )
            )
        else:
            registration_expires_at = (
                registration.expires_at
            )

        existing_otp = (
            self.repository.get_pending_otp(
                registration.registration_id
            )
        )

        if existing_otp:
            self.repository.mark_otp_failed(
                existing_otp
            )

        otp = self.generate_otp()

        otp_hash = self.password_hash.hash(
            otp
        )

        otp_expires_at = (
            now + timedelta(minutes=10)
        )

        self.repository.create_verification(
            registration_id=registration.registration_id,
            otp_hash=otp_hash,
            expires_at=otp_expires_at
        )

        registration.registration_status = (
            "OTP_PENDING"
        )

        sms_result = self.send_otp(
            mobile_number=customer.mobile_number,
            otp=otp
        )

        if not sms_result["success"]:
            self.db.rollback()

            return {
                "success": False,
                "message": (
                    "Account was verified, "
                    "but OTP could not be sent. "
                    "Please try again."
                )
            }

        self.db.commit()

        return {
            "success": True,
            "message": (
                "Account verified successfully. "
                "OTP has been sent to your "
                "registered mobile number."
            ),
            "registration_id": (
                registration.registration_id
            ),
            "next_step": "OTP_PENDING",
            "registration_expires_at": (
                registration_expires_at
            )
        }

    def resend_otp(
        self,
        registration_id: int
    ):
        registration = (
            self.repository.get_registration(
                registration_id
            )
        )

        if not registration:
            return {
                "success": False,
                "message": "Registration not found."
            }

        now = datetime.utcnow()

        if (
            registration.registration_status
            == "REGISTERED"
        ):
            return {
                "success": False,
                "message": (
                    "Registration is already "
                    "completed."
                )
            }

        if registration.expires_at <= now:
            self.repository.delete_expired_registration(
                registration.registration_id
            )

            self.db.commit()

            return {
                "success": False,
                "message": (
                    "Registration has expired. "
                    "Please start registration again."
                )
            }

        if (
            registration.registration_status
            != "OTP_PENDING"
        ):
            return {
                "success": False,
                "message": (
                    "Resend OTP is not available "
                    "for this registration."
                )
            }

        customer = (
            self.repository.get_customer_by_registration(
                registration_id
            )
        )

        if not customer:
            return {
                "success": False,
                "message": "Customer not found."
            }

        existing_otp = (
            self.repository.get_pending_otp(
                registration_id
            )
        )

        if existing_otp:
            self.repository.mark_otp_failed(
                existing_otp
            )

        otp = self.generate_otp()

        otp_hash = self.password_hash.hash(
            otp
        )

        otp_expires_at = (
            now + timedelta(minutes=10)
        )

        self.repository.create_verification(
            registration_id=registration_id,
            otp_hash=otp_hash,
            expires_at=otp_expires_at
        )

        sms_result = self.send_otp(
            mobile_number=customer.mobile_number,
            otp=otp
        )

        if not sms_result["success"]:
            self.db.rollback()

            return {
                "success": False,
                "message": (
                    "New OTP could not be sent. "
                    "Please try again."
                )
            }

        self.db.commit()

        return {
            "success": True,
            "message": (
                "A new OTP has been sent to your "
                "registered mobile number."
            ),
            "registration_id": registration_id,
            "next_step": "OTP_PENDING"
        }

    def verify_phone(
        self,
        registration_id: int,
        otp: str
    ):
        registration = (
            self.repository.get_registration(
                registration_id
            )
        )

        if not registration:
            return {
                "success": False,
                "message": "Registration not found."
            }

        now = datetime.utcnow()

        if (
            registration.registration_status
            != "REGISTERED"
            and registration.expires_at <= now
        ):
            self.repository.delete_expired_registration(
                registration.registration_id
            )

            self.db.commit()

            return {
                "success": False,
                "message": (
                    "Registration has expired. "
                    "Please start registration again."
                )
            }

        if (
            registration.registration_status
            == "REGISTERED"
        ):
            return {
                "success": False,
                "message": (
                    "Registration is already "
                    "completed."
                )
            }

        if (
            registration.registration_status
            != "OTP_PENDING"
        ):
            return {
                "success": False,
                "message": (
                    "OTP verification is not available "
                    "for this registration."
                )
            }

        if not otp.isdigit() or len(otp) != 6:
            return {
                "success": False,
                "message": (
                    "OTP must be exactly 6 digits."
                )
            }

        verification = (
            self.repository.get_pending_otp(
                registration_id
            )
        )

        if not verification:
            return {
                "success": False,
                "message": (
                    "No active OTP was found. "
                    "Please request a new OTP."
                )
            }

        if verification.expires_at <= now:
            self.repository.mark_otp_expired(
                verification
            )

            self.db.commit()

            return {
                "success": False,
                "message": (
                    "OTP has expired. "
                    "Please request a new OTP."
                )
            }

        if verification.attempt_count >= 5:
            self.repository.mark_otp_failed(
                verification
            )

            self.db.commit()

            return {
                "success": False,
                "message": (
                    "Too many incorrect OTP attempts. "
                    "Please request a new OTP."
                )
            }

        is_valid = self.password_hash.verify(
            otp,
            verification.otp_hash
        )

        if not is_valid:
            self.repository.increment_otp_attempt(
                verification
            )

            self.db.commit()

            remaining_attempts = (
                5 - verification.attempt_count
            )

            return {
                "success": False,
                "message": (
                    f"Invalid OTP. "
                    f"{remaining_attempts} "
                    f"attempts remaining."
                )
            }

        self.repository.mark_otp_verified(
            verification,
            now
        )

        registration.otp_verified_at = now

        registration.registration_status = (
            "MPIN_SETUP_PENDING"
        )

        self.db.commit()

        return {
            "success": True,
            "message": (
                "Mobile number verified "
                "successfully."
            ),
            "registration_id": (
                registration.registration_id
            ),
            "next_step": "MPIN_SETUP"
        }

    def setup_mpin(
        self,
        registration_id: int,
        mpin: str
    ):
        registration = (
            self.repository.get_registration(
                registration_id
            )
        )

        if not registration:
            return {
                "success": False,
                "message": "Registration not found."
            }

        now = datetime.utcnow()

        if (
            registration.registration_status
            != "REGISTERED"
            and registration.expires_at <= now
        ):
            self.repository.delete_expired_registration(
                registration.registration_id
            )

            self.db.commit()

            return {
                "success": False,
                "message": (
                    "Registration has expired. "
                    "Please start registration again."
                )
            }

        if (
            registration.registration_status
            != "MPIN_SETUP_PENDING"
        ):
            return {
                "success": False,
                "message": (
                    "MPIN setup is not available "
                    "for this registration."
                )
            }

        if not mpin.isdigit() or len(mpin) != 6:
            return {
                "success": False,
                "message": (
                    "MPIN must be exactly 6 digits."
                )
            }

        customer = (
            self.repository.get_customer_by_registration(
                registration_id
            )
        )

        if not customer:
            return {
                "success": False,
                "message": (
                    "Customer could not be found."
                )
            }

        existing_credential = (
            self.repository.get_credential_by_customer_id(
                customer.customer_id
            )
        )

        if existing_credential:
            return {
                "success": False,
                "message": (
                    "Customer credentials "
                    "already exist."
                )
            }

        hashed_mpin = (
            self.password_hash.hash(
                mpin
            )
        )

        self.repository.create_customer_credential(
            customer_id=customer.customer_id,
            mpin_hash=hashed_mpin,
            created_at=now
        )

        registration.mpin_setup_at = now

        registration.registration_status = (
            "REGISTERED"
        )

        registration.registration_completed_at = now

        self.db.commit()

        return {
            "success": True,
            "message": (
                "MPIN created successfully. "
                "Registration completed."
            ),
            "registration_id": (
                registration.registration_id
            ),
            "next_step": "LOGIN"
        }