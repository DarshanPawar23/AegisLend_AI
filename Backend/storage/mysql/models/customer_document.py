from sqlalchemy import Column, BigInteger, String, Date, DateTime, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from storage.mysql.base import Base


class CustomerDocument(Base):
    __tablename__ = "customer_documents"

    document_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("bank_customers.customer_id"),
        nullable=False
    )

    document_type = Column(
        Enum(
            "SALARY_SLIP",
            "BANK_STATEMENT",
            "FORM_16",
            "ITR",
            "APPOINTMENT_LETTER",
            "EMPLOYEE_ID",
            "PROFESSIONAL_CERTIFICATE",
            "BUSINESS_REGISTRATION",
            "GST_CERTIFICATE",
            "MSME_CERTIFICATE",
            "BALANCE_SHEET",
            "PROFIT_LOSS_STATEMENT",
            "AUDIT_REPORT",
            "GST_RETURN",
            "BUSINESS_BANK_STATEMENT",
            "BUSINESS_CONTINUITY_PROOF",
            "ACADEMIC_MARKSHEET",
            "ADMISSION_LETTER",
            "PASSPORT",
            "VISA",
            "I20_CAS",
            "PENSION_PAYMENT_ORDER",
            "PENSION_SLIP",
            "FD_CERTIFICATE",
            "PROPERTY_DOCUMENT",
            "GOLD_VALUATION",
            "AFFIDAVIT",
            "LAND_RECORD",
            "KCC_RECORD",
            "PLATFORM_EARNING_REPORT",
            "FORM_26AS",
            "OTHER"
        ),
        nullable=False
    )

    document_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(String(500))
    file_hash = Column(String(128))

    issue_date = Column(Date)
    expiry_date = Column(Date)

    document_status = Column(
        Enum(
            "UPLOADED",
            "UNDER_REVIEW",
            "VERIFIED",
            "REJECTED",
            "EXPIRED"
        ),
        default="UPLOADED"
    )

    uploaded_at = Column(DateTime)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    customer = relationship(
        "BankCustomer",
        back_populates="documents"
    )