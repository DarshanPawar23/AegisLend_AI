from sqlalchemy import Column, BigInteger, String, Integer, DateTime, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerCredential(Base):
    __tablename__ = "customer_credentials"

    credential_id = Column(
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

    mpin_hash = Column(
        String(255),
        nullable=False
    )

    mpin_failed_attempts = Column(
        Integer,
        default=0
    )

    mpin_locked_until = Column(DateTime)

    last_mpin_changed_at = Column(DateTime)

    credential_status = Column(
        Enum("ACTIVE", "LOCKED", "DISABLED"),
        default="ACTIVE"
    )

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    customer = relationship(
        "BankCustomer",
        back_populates="credentials"
    )