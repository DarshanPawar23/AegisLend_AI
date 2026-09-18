from sqlalchemy import Column, BigInteger, String, DateTime, DECIMAL, ForeignKey, Enum
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerSession(Base):
    __tablename__ = "customer_sessions"

    session_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False
    )

    session_token_hash = Column(
        String(255),
        nullable=False,
        unique=True
    )

    device_id = Column(String(255))
    device_name = Column(String(150))

    ip_address = Column(String(45))
    user_agent = Column(String(500))

    login_latitude = Column(DECIMAL(10, 7))
    login_longitude = Column(DECIMAL(10, 7))
    login_city = Column(String(100))
    login_country = Column(String(100))

    login_at = Column(DateTime)
    last_activity_at = Column(DateTime)
    logout_at = Column(DateTime)

    session_status = Column(
        Enum(
            "ACTIVE",
            "ENDED",
            "TERMINATED",
            "EXPIRED"
        ),
        default="ACTIVE"
    )

    termination_reason = Column(String(255))

    customer = relationship(
        "BankCustomer",
        back_populates="sessions"
    )