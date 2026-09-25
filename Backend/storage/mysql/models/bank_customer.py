from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Date,
    Enum,
    TIMESTAMP
)

from sqlalchemy.orm import relationship

from storage.mysql.base import Base


class BankCustomer(Base):

    __tablename__ = "bank_customers"

    customer_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_number = Column(
        String(20),
        nullable=False,
        unique=True
    )

    account_number = Column(
        String(20),
        nullable=False,
        unique=True
    )

    first_name = Column(
        String(50),
        nullable=False
    )

    middle_name = Column(
        String(50),
        nullable=True
    )

    last_name = Column(
        String(50),
        nullable=False
    )

    date_of_birth = Column(
        Date,
        nullable=False
    )

    gender = Column(
        Enum(
            "MALE",
            "FEMALE",
            "OTHER"
        ),
        nullable=True
    )

    email = Column(
        String(150),
        unique=True,
        nullable=True
    )

    mobile_number = Column(
        String(15),
        nullable=False,
        unique=True
    )

    alternate_mobile = Column(
        String(15),
        nullable=True
    )

    account_type = Column(
        Enum(
            "SAVINGS",
            "CURRENT",
            "SALARY",
            "NRI"
        ),
        nullable=False
    )

    account_status = Column(
        Enum(
            "ACTIVE",
            "DORMANT",
            "BLOCKED",
            "CLOSED"
        ),
        nullable=False,
        default="ACTIVE"
    )

    account_opening_date = Column(
        Date,
        nullable=False
    )

    customer_since = Column(
        Date,
        nullable=True
    )

    branch_code = Column(
        String(20),
        nullable=True
    )

    branch_name = Column(
        String(100),
        nullable=True
    )

    ifsc_code = Column(
        String(20),
        nullable=True
    )

    profile_image_url = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP
    )

    updated_at = Column(
        TIMESTAMP
    )

    addresses = relationship(
        "CustomerAddress",
        back_populates="customer"
    )

    kyc = relationship(
        "CustomerKYC",
        back_populates="customer",
        uselist=False
    )

    employments = relationship(
        "CustomerEmployment",
        back_populates="customer"
    )

    incomes = relationship(
        "CustomerIncome",
        back_populates="customer"
    )

    financial_profile = relationship(
        "CustomerFinancialProfile",
        back_populates="customer",
        uselist=False
    )

    credentials = relationship(
        "CustomerCredential",
        back_populates="customer",
        uselist=False
    )

    login_attempts = relationship(
        "LoginAttempt",
        back_populates="customer"
    )

    sessions = relationship(
        "CustomerSession",
        back_populates="customer"
    )

    documents = relationship(
        "CustomerDocument",
        back_populates="customer"
    )

    loans = relationship(
        "CustomerLoan",
        back_populates="customer"
    )

    loan_payments = relationship(
        "LoanPayment",
        back_populates="customer"
    )

    app_registration = relationship(
        "UserAppRegistration",
        back_populates="customer",
        uselist=False
    )

    login_otp_verifications = relationship(
        "LoginOtpVerification",
        back_populates="customer"
    )