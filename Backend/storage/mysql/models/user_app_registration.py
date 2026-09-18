from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    TIMESTAMP,
    ForeignKey,
    Enum,
    text
)
from sqlalchemy.orm import relationship

from storage.mysql.base import Base


class UserAppRegistration(Base):
    __tablename__ = "user_app_registrations"

    registration_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False,
        unique=True
    )

    registration_status = Column(
        Enum(
            "ACCOUNT_VERIFIED",
            "OTP_PENDING",
            "MPIN_SETUP_PENDING",
            "REGISTERED",
            "BLOCKED",
            "CANCELLED"
        ),
        nullable=False,
        default="ACCOUNT_VERIFIED"
    )

    account_verified_at = Column(
        DateTime,
        nullable=True
    )

    otp_verified_at = Column(
        DateTime,
        nullable=True
    )

    mpin_setup_at = Column(
        DateTime,
        nullable=True
    )

    registration_completed_at = Column(
        DateTime,
        nullable=True
    )

    # Registration must be completed before this time.
    # Service will set this to created time + 24 hours.
    expires_at = Column(
        DateTime,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP")
    )

    customer = relationship(
        "BankCustomer",
        back_populates="app_registration"
    )

    verifications = relationship(
        "RegistrationVerification",
        back_populates="registration"
    )