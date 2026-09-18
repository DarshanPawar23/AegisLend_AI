from sqlalchemy import Column, BigInteger, String, Integer, Date, DateTime, TIMESTAMP, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class LoanPayment(Base):
    __tablename__ = "loan_payments"

    payment_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    loan_id = Column(
        BigInteger,
        ForeignKey("customer_loans.loan_id"),
        nullable=False
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False
    )

    payment_reference = Column(
        String(50),
        nullable=False,
        unique=True
    )

    installment_number = Column(Integer)

    due_date = Column(Date)
    payment_date = Column(Date)

    principal_amount = Column(DECIMAL(15, 2))
    interest_amount = Column(DECIMAL(15, 2))
    penalty_amount = Column(DECIMAL(15, 2))
    total_amount = Column(DECIMAL(15, 2))

    payment_method = Column(
        Enum(
            "AUTO_DEBIT",
            "BANK_TRANSFER",
            "UPI",
            "CASH",
            "CHEQUE",
            "CARD",
            "OTHER"
        )
    )

    payment_status = Column(
        Enum(
            "PAID",
            "PARTIALLY_PAID",
            "MISSED",
            "LATE",
            "FAILED",
            "REFUNDED"
        ),
        nullable=False
    )

    days_late = Column(
        Integer,
        default=0
    )

    transaction_reference = Column(
        String(100)
    )

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    loan = relationship(
        "CustomerLoan",
        back_populates="payments"
    )

    customer = relationship(
        "BankCustomer",
        back_populates="loan_payments"
    )