from sqlalchemy import Column, BigInteger, String, Integer, Boolean, DateTime, TIMESTAMP, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerFinancialProfile(Base):
    __tablename__ = "customer_financial_profile"

    financial_profile_id = Column(
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

    credit_score = Column(Integer)
    credit_score_provider = Column(String(50))
    credit_score_updated_at = Column(DateTime)

    total_existing_debt = Column(
        DECIMAL(15, 2),
        default=0.00
    )

    monthly_emi_obligation = Column(
        DECIMAL(15, 2),
        default=0.00
    )

    debt_to_income_ratio = Column(
        DECIMAL(5, 2)
    )

    total_loans_taken = Column(Integer, default=0)
    active_loans_count = Column(Integer, default=0)
    completed_loans_count = Column(Integer, default=0)
    defaulted_loans_count = Column(Integer, default=0)

    total_loan_amount = Column(
        DECIMAL(15, 2),
        default=0.00
    )

    total_outstanding_loan_amount = Column(
        DECIMAL(15, 2),
        default=0.00
    )

    total_emi_paid = Column(Integer, default=0)
    total_emi_missed = Column(Integer, default=0)
    late_payment_count = Column(Integer, default=0)

    repayment_history_score = Column(
        DECIMAL(5, 2)
    )

    risk_category = Column(
        Enum("LOW", "MEDIUM", "HIGH"),
        default="LOW"
    )

    fraud_flag = Column(
        Boolean,
        default=False
    )

    last_financial_reviewed_at = Column(DateTime)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    customer = relationship(
        "BankCustomer",
        back_populates="financial_profile"
    )