from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Date, TIMESTAMP, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerLoan(Base):
    __tablename__ = "customer_loans"

    loan_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False
    )

    loan_account_number = Column(
        String(30),
        nullable=False,
        unique=True
    )

    loan_type = Column(
        Enum(
            "PERSONAL",
            "HOME",
            "EDUCATION",
            "VEHICLE",
            "GOLD",
            "BUSINESS",
            "AGRICULTURE",
            "OTHER"
        ),
        nullable=False
    )

    loan_purpose = Column(String(255))

    application_date = Column(Date)
    approval_date = Column(Date)
    sanction_date = Column(Date)
    disbursement_date = Column(Date)

    sanctioned_amount = Column(DECIMAL(15, 2))
    disbursed_amount = Column(DECIMAL(15, 2))

    interest_rate = Column(DECIMAL(5, 2))

    interest_type = Column(
        Enum("FIXED", "FLOATING")
    )

    tenure_months = Column(Integer)

    emi_amount = Column(DECIMAL(15, 2))

    processing_fee = Column(DECIMAL(15, 2))
    insurance_amount = Column(DECIMAL(15, 2))
    other_charges = Column(DECIMAL(15, 2))

    total_repayment_amount = Column(DECIMAL(15, 2))
    total_amount_paid = Column(
        DECIMAL(15, 2),
        default=0.00
    )

    outstanding_principal = Column(
        DECIMAL(15, 2),
        default=0.00
    )

    outstanding_interest = Column(
        DECIMAL(15, 2),
        default=0.00
    )

    loan_start_date = Column(Date)
    expected_end_date = Column(Date)
    actual_end_date = Column(Date)

    total_emi_count = Column(Integer)
    paid_emi_count = Column(Integer, default=0)
    pending_emi_count = Column(Integer, default=0)
    missed_emi_count = Column(Integer, default=0)
    late_payment_count = Column(Integer, default=0)

    collateral_required = Column(
        Boolean,
        default=False
    )

    collateral_type = Column(String(100))
    collateral_value = Column(DECIMAL(15, 2))

    guarantor_required = Column(
        Boolean,
        default=False
    )

    guarantor_name = Column(String(150))

    loan_status = Column(
        Enum(
            "PENDING",
            "APPROVED",
            "ACTIVE",
            "CLOSED",
            "REJECTED",
            "DEFAULTED",
            "SETTLED",
            "RESTRUCTURED",
            "CANCELLED"
        ),
        nullable=False
    )

    repayment_status = Column(
        Enum(
            "CURRENT",
            "OVERDUE",
            "DEFAULTED",
            "COMPLETED"
        ),
        default="CURRENT"
    )

    days_past_due = Column(
        Integer,
        default=0
    )

    last_payment_date = Column(Date)
    next_payment_date = Column(Date)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    customer = relationship(
        "BankCustomer",
        back_populates="loans"
    )

    payments = relationship(
        "LoanPayment",
        back_populates="loan"
    )