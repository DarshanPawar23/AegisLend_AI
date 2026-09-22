from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    DateTime,
    TIMESTAMP,
    ForeignKey,
    Enum
)

from sqlalchemy.orm import relationship

from storage.mysql.base import Base


class RegistrationVerification(Base):

    __tablename__ = "registration_verifications"

    verification_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    registration_id = Column(
        BigInteger,
        ForeignKey(
            "user_app_registrations.registration_id"
        ),
        nullable=False
    )

    verification_type = Column(
        Enum("MOBILE_OTP"),
        nullable=False
    )

    otp_hash = Column(
        String(255),
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    verified_at = Column(
        DateTime,
        nullable=True
    )

    attempt_count = Column(
        Integer,
        nullable=False,
        default=0
    )

    verification_status = Column(
        Enum(
            "PENDING",
            "VERIFIED",
            "EXPIRED",
            "FAILED",
            "CANCELLED"
        ),
        nullable=False,
        default="PENDING"
    )

    created_at = Column(
        TIMESTAMP,
        nullable=True
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=True
    )

    registration = relationship(
        "UserAppRegistration",
        back_populates="verifications"
    )