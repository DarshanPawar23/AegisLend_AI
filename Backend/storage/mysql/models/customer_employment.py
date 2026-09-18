from sqlalchemy import Column, BigInteger, String, Date, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerEmployment(Base):
    __tablename__ = "customer_employment"

    employment_id = Column(BigInteger, primary_key=True, autoincrement=True)

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False
    )

    employment_type = Column(
        Enum(
            "SALARIED",
            "SELF_EMPLOYED",
            "BUSINESS",
            "STUDENT",
            "RETIRED",
            "UNEMPLOYED",
            "OTHER"
        ),
        nullable=False
    )

    employer_name = Column(String(150))
    job_title = Column(String(100))
    business_name = Column(String(150))
    profession = Column(String(100))

    employment_start_date = Column(Date)
    employment_end_date = Column(Date)

    employment_status = Column(
        Enum("CURRENT", "PREVIOUS"),
        default="CURRENT"
    )

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    customer = relationship(
        "BankCustomer",
        back_populates="employments"
    )

    incomes = relationship(
        "CustomerIncome",
        back_populates="employment"
    )