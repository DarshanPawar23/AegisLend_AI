from datetime import datetime, timedelta

from firebase_admin import auth
from sqlalchemy.orm import Session

from repositories.user_repository.user_registration import (
    UserRegistrationRepository
)


class UserRegistrationService:

    def __init__(self, db: Session):

        self.db = db

        self.repository = (
            UserRegistrationRepository(db)
        )

    # =========================================================
    # STEP 1
    # VERIFY BANK ACCOUNT DETAILS
    # =========================================================

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

        # -----------------------------------------------------
        # CUSTOMER NOT FOUND
        # -----------------------------------------------------

        if not customer:

            return {
                "success": False,
                "message": (
                    "The provided account details "
                    "could not be verified."
                )
            }

        # -----------------------------------------------------
        # ACCOUNT NOT ACTIVE
        # -----------------------------------------------------

        if customer.account_status != "ACTIVE":

            return {
                "success": False,
                "message": (
                    "The bank account is not active."
                )
            }

        # -----------------------------------------------------
        # CHECK EXISTING REGISTRATION
        # -----------------------------------------------------

        registration = (
            self.repository
            .get_registration_by_customer_id(
                customer.customer_id
            )
        )

        now = datetime.utcnow()

        # -----------------------------------------------------
        # DELETE EXPIRED INCOMPLETE REGISTRATION
        # -----------------------------------------------------

        if registration:

            if (
                registration.registration_status
                != "REGISTERED"
                and registration.expires_at <= now
            ):

                self.repository.delete_expired_registration(
                    registration.registration_id
                )

                self.db.commit()

                registration = None

        # -----------------------------------------------------
        # ALREADY REGISTERED
        # -----------------------------------------------------

        if registration:

            if (
                registration.registration_status
                == "REGISTERED"
            ):

                return {
                    "success": False,
                    "message": (
                        "This account is already registered."
                    )
                }

            # Registration is still active

            return {
                "success": True,
                "message": (
                    "Registration already in progress."
                ),
                "registration_id":
                    registration.registration_id,
                "next_step":
                    registration.registration_status
            }

        # -----------------------------------------------------
        # CREATE NEW REGISTRATION
        # -----------------------------------------------------

        expires_at = (
            now + timedelta(hours=24)
        )

        registration = (
            self.repository.create_registration(
                customer_id=customer.customer_id,
                expires_at=expires_at
            )
        )

        self.db.commit()

        return {
            "success": True,
            "message": (
                "Account verified successfully."
            ),
            "registration_id":
                registration.registration_id,
            "next_step":
                "OTP_PENDING",
            "registration_expires_at":
                expires_at
        }

    # =========================================================
    # STEP 2
    # VERIFY FIREBASE PHONE AUTHENTICATION
    # =========================================================

    def verify_phone(
        self,
        registration_id: int,
        firebase_id_token: str
    ):

        # -----------------------------------------------------
        # GET REGISTRATION
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # CHECK 24-HOUR REGISTRATION EXPIRY
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # ALREADY REGISTERED
        # -----------------------------------------------------

        if (
            registration.registration_status
            == "REGISTERED"
        ):

            return {
                "success": False,
                "message": (
                    "Registration is already completed."
                )
            }

        # -----------------------------------------------------
        # VERIFY FIREBASE ID TOKEN
        # -----------------------------------------------------

        try:

            decoded_token = (
                auth.verify_id_token(
                    firebase_id_token
                )
            )

        except Exception:

            return {
                "success": False,
                "message": (
                    "Firebase phone verification "
                    "could not be verified."
                )
            }

        # -----------------------------------------------------
        # GET PHONE FROM FIREBASE TOKEN
        # -----------------------------------------------------

        firebase_phone = (
            decoded_token.get("phone_number")
        )

        if not firebase_phone:

            return {
                "success": False,
                "message": (
                    "Verified phone number "
                    "was not found."
                )
            }

        # -----------------------------------------------------
        # GET BANK CUSTOMER
        # -----------------------------------------------------

        customer = (
            self.repository
            .get_customer_by_registration(
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

        # -----------------------------------------------------
        # NORMALIZE PHONE NUMBERS
        # -----------------------------------------------------

        database_phone = (
            customer.mobile_number
            .replace(" ", "")
            .replace("-", "")
        )

        firebase_phone = (
            firebase_phone
            .replace(" ", "")
            .replace("-", "")
        )

        # -----------------------------------------------------
        # COMPARE PHONE NUMBERS
        # -----------------------------------------------------

        if not firebase_phone.endswith(
            database_phone
        ):

            return {
                "success": False,
                "message": (
                    "The verified phone number "
                    "does not match the registered "
                    "bank mobile number."
                )
            }

        # -----------------------------------------------------
        # MOBILE VERIFICATION SUCCESS
        # -----------------------------------------------------

        registration.otp_verified_at = now

        registration.registration_status = (
            "MPIN_SETUP_PENDING"
        )

        self.db.commit()

        return {
            "success": True,
            "message": (
                "Mobile number verified successfully."
            ),
            "registration_id":
                registration.registration_id,
            "next_step":
                "MPIN_SETUP"
        }