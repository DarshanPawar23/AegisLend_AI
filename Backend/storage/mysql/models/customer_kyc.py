from sqlalchemy import Column, BigInteger, String, Date, DateTime, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerKYC(Base):
    __tablename__ = "customer_kyc"

    kyc_id = Column(BigInteger, primary_key=True, autoincrement=True)

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False,
        unique=True
    )

    pan_number = Column(String(20))
    aadhaar_reference = Column(String(100))

    kyc_status = Column(
        Enum("VERIFIED", "PENDING", "EXPIRED", "REJECTED"),
        default="PENDING"
    )

    kyc_verified_at = Column(DateTime)
    kyc_expiry_date = Column(Date)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    customer = relationship(
        "BankCustomer",
        back_populates="kyc"
    )