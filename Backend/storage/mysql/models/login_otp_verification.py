from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    DateTime,
    TIMESTAMP,
    ForeignKey,
    Enum,
    text
)

from sqlalchemy.orm import relationship

from storage.mysql.base import Base


class LoginOtpVerification(Base):

    __tablename__ = "login_otp_verifications"

    login_otp_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey(
            "bank_customers.customer_id",
            ondelete="CASCADE"
        ),
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
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text(
            "CURRENT_TIMESTAMP"
        )
    )

    customer = relationship(
        "BankCustomer",
        back_populates="login_otp_verifications"
    )

