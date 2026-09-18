from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    address_id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False
    )

    address_type = Column(
        Enum("PERMANENT", "CURRENT", "OFFICE"),
        nullable=False
    )

    address_line1 = Column(String(150), nullable=False)
    address_line2 = Column(String(150))

    city = Column(String(100), nullable=False)
    district = Column(String(100))
    state = Column(String(100), nullable=False)
    country = Column(String(100), default="India")
    pincode = Column(String(10), nullable=False)

    is_current = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    customer = relationship(
        "BankCustomer",
        back_populates="addresses"
    )