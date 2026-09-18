from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    attempt_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id")
    )

    attempted_at = Column(
        DateTime
    )

    ip_address = Column(String(45))
    device_id = Column(String(255))
    user_agent = Column(String(500))

    attempt_status = Column(
        Enum(
            "SUCCESS",
            "FAILED",
            "BLOCKED",
            "OTP_REQUIRED",
            "CHALLENGE_REQUIRED"
        ),
        nullable=False
    )

    failure_reason = Column(String(255))

    customer = relationship(
        "BankCustomer",
        back_populates="login_attempts"
    )