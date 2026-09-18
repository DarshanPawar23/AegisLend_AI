from sqlalchemy import Column, BigInteger, String, Date, DateTime, TIMESTAMP, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerIncome(Base):
    __tablename__ = "customer_income"

    income_id = Column(BigInteger, primary_key=True, autoincrement=True)

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False
    )

    employment_id = Column(
        BigInteger,
        ForeignKey("customer_employment.employment_id")
    )

    income_type = Column(
        Enum(
            "SALARY",
            "BUSINESS",
            "PROFESSIONAL",
            "PENSION",
            "AGRICULTURE",
            "FREELANCE",
            "RENTAL",
            "INVESTMENT",
            "OTHER"
        ),
        nullable=False
    )

    monthly_income = Column(DECIMAL(15, 2))
    annual_income = Column(DECIMAL(15, 2))

    income_start_date = Column(Date)
    income_end_date = Column(Date)

    income_status = Column(
        Enum("CURRENT", "PREVIOUS"),
        default="CURRENT"
    )

    verification_status = Column(
        Enum("VERIFIED", "PENDING", "REJECTED"),
        default="PENDING"
    )

    verified_at = Column(DateTime)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    customer = relationship(
        "BankCustomer",
        back_populates="incomes"
    )

    employment = relationship(
        "CustomerEmployment",
        back_populates="incomes"
    )