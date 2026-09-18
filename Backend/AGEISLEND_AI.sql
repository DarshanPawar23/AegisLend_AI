CREATE DATABASE aegislend;
USE aegislend;
CREATE DATABASE aegislend;

USE aegislend;

CREATE TABLE bank_customers (
    customer_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_number VARCHAR(20) NOT NULL UNIQUE,
    account_number VARCHAR(20) NOT NULL UNIQUE,

    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,

    date_of_birth DATE NOT NULL,
    gender ENUM('MALE', 'FEMALE', 'OTHER'),

    email VARCHAR(150) UNIQUE,
    mobile_number VARCHAR(15) NOT NULL UNIQUE,
    alternate_mobile VARCHAR(15),
    account_type ENUM(
        'SAVINGS',
        'CURRENT',
        'SALARY',
        'NRI'
    ) NOT NULL,
    
    account_status ENUM(
        'ACTIVE',
        'DORMANT',
        'BLOCKED',
        'CLOSED'
    ) NOT NULL DEFAULT 'ACTIVE',

    account_opening_date DATE NOT NULL,
    customer_since DATE,

    branch_code VARCHAR(20),
    branch_name VARCHAR(100),
    ifsc_code VARCHAR(20),

    profile_image_url VARCHAR(500),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
INSERT INTO bank_customers
(customer_id, customer_number, account_number, first_name, middle_name, last_name,
date_of_birth, gender, email, mobile_number, alternate_mobile,
account_type, account_status, account_opening_date, customer_since,
branch_code, branch_name, ifsc_code, profile_image_url)
VALUES
(1001, 'CUST1001', 'AEGIS10010001', 'Arjun', NULL, 'Mehta',
'1999-04-18', 'MALE', 'arjun.mehta@example.com', '9000001001', NULL,
'SAVINGS', 'ACTIVE', '2021-07-14', '2021-07-14',
'AGB001', 'Aegis Central Branch', 'AEGIS000001', '/storage/customer-profiles/CUST1001.jpg'),

(1002, 'CUST1002', 'AEGIS10010002', 'Priya', NULL, 'Sharma',
'1992-11-06', 'FEMALE', 'priya.sharma@example.com', '9000001002', NULL,
'SALARY', 'ACTIVE', '2018-03-22', '2018-03-22',
'AGB002', 'Aegis Business Branch', 'AEGIS000002', '/storage/customer-profiles/CUST1002.jpg'),

(1003, 'CUST1003', 'AEGIS10010003', 'Vikram', 'Raj', 'Patil',
'1987-08-25', 'MALE', 'vikram.patil@example.com', '9000001003', NULL,
'CURRENT', 'ACTIVE', '2019-10-11', '2019-10-11',
'AGB003', 'Aegis Market Branch', 'AEGIS000003', '/storage/customer-profiles/CUST1003.jpg');

CREATE TABLE customer_addresses (
    address_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,

    address_type ENUM(
        'PERMANENT',
        'CURRENT',
        'OFFICE'
    ) NOT NULL,

    address_line1 VARCHAR(150) NOT NULL,
    address_line2 VARCHAR(150),

    city VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) DEFAULT 'India',
    pincode VARCHAR(10) NOT NULL,

    is_current BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);
INSERT INTO customer_addresses
(address_id, customer_id, address_type, address_line1, address_line2,
city, district, state, country, pincode, is_current)
VALUES
(2001, 1001, 'PERMANENT',
'24 Green Park Road', 'Vidyanagar',
'Hubballi', 'Dharwad', 'Karnataka', 'India', '580021', TRUE),

(2002, 1002, 'PERMANENT',
'18 Lake View Residency', 'Indiranagar',
'Bengaluru', 'Bengaluru Urban', 'Karnataka', 'India', '560038', TRUE),

(2003, 1003, 'PERMANENT',
'42 Market Road', 'Tilakwadi',
'Belagavi', 'Belagavi', 'Karnataka', 'India', '590006', TRUE);

CREATE TABLE customer_kyc (
    kyc_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL UNIQUE,
    pan_number VARCHAR(20),
    aadhaar_reference VARCHAR(100),
    kyc_status ENUM(
        'VERIFIED',
        'PENDING',
        'EXPIRED',
        'REJECTED'
    ) DEFAULT 'PENDING',
    kyc_verified_at DATETIME,
    kyc_expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);
INSERT INTO customer_kyc
(kyc_id, customer_id, pan_number, aadhaar_reference,
kyc_status, kyc_verified_at, kyc_expiry_date)
VALUES
(3001, 1001, 'ABCDE1234F', 'AADHAAR-REF-1001',
'VERIFIED', '2021-07-15 11:20:00', NULL),

(3002, 1002, 'BCDEF2345G', 'AADHAAR-REF-1002',
'VERIFIED', '2018-03-23 10:15:00', NULL),

(3003, 1003, 'CDEFG3456H', 'AADHAAR-REF-1003',
'VERIFIED', '2019-10-12 14:05:00', NULL);

CREATE TABLE customer_employment (
    employment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    employment_type ENUM(
        'SALARIED',
        'SELF_EMPLOYED',
        'BUSINESS',
        'STUDENT',
        'RETIRED',
        'UNEMPLOYED',
        'OTHER'
    ) NOT NULL,
    employer_name VARCHAR(150),
    job_title VARCHAR(100),
    business_name VARCHAR(150),
    profession VARCHAR(100),

    employment_start_date DATE,
    employment_end_date DATE,

    employment_status ENUM(
        'CURRENT',
        'PREVIOUS'
    ) DEFAULT 'CURRENT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);
INSERT INTO customer_employment
(employment_id, customer_id, employment_type, employer_name,
job_title, business_name, profession,
employment_start_date, employment_end_date, employment_status)
VALUES
(4001, 1001, 'SALARIED', 'TechNova Solutions Pvt Ltd',
'Software Engineer', NULL, NULL,
'2022-08-01', NULL, 'CURRENT'),

(4002, 1002, 'SALARIED', 'Global Finance Services Ltd',
'Senior Financial Analyst', NULL, NULL,
'2019-06-10', NULL, 'CURRENT'),

(4003, 1003, 'BUSINESS', NULL,
NULL, 'Patil Electricals', 'Business Owner',
'2015-04-01', NULL, 'CURRENT');

CREATE TABLE customer_income (
    income_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    employment_id BIGINT,

    income_type ENUM(
        'SALARY',
        'BUSINESS',
        'PROFESSIONAL',
        'PENSION',
        'AGRICULTURE',
        'FREELANCE',
        'RENTAL',
        'INVESTMENT',
        'OTHER'
    ) NOT NULL,

    monthly_income DECIMAL(15,2),
    annual_income DECIMAL(15,2),

    income_start_date DATE,
    income_end_date DATE,

    income_status ENUM(
        'CURRENT',
        'PREVIOUS'
    ) DEFAULT 'CURRENT',

    verification_status ENUM(
        'VERIFIED',
        'PENDING',
        'REJECTED'
    ) DEFAULT 'PENDING',

    verified_at DATETIME,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id),

    FOREIGN KEY (employment_id)
        REFERENCES customer_employment(employment_id)
);
INSERT INTO customer_income
(income_id, customer_id, employment_id, income_type,
monthly_income, annual_income,
income_start_date, income_end_date,
income_status, verification_status, verified_at)
VALUES
(5001, 1001, 4001, 'SALARY',
65000.00, 780000.00,
'2026-01-01', NULL,
'CURRENT', 'VERIFIED', '2026-08-05 10:30:00'),

(5002, 1002, 4002, 'SALARY',
105000.00, 1260000.00,
'2026-01-01', NULL,
'CURRENT', 'VERIFIED', '2026-08-03 11:15:00'),

(5003, 1003, 4003, 'BUSINESS',
180000.00, 2160000.00,
'2026-01-01', NULL,
'CURRENT', 'VERIFIED', '2026-08-08 15:40:00');

CREATE TABLE customer_financial_profile (
    financial_profile_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL UNIQUE,

    credit_score INT,
    credit_score_provider VARCHAR(50),
    credit_score_updated_at DATETIME,

    total_existing_debt DECIMAL(15,2) DEFAULT 0.00,
    monthly_emi_obligation DECIMAL(15,2) DEFAULT 0.00,

    debt_to_income_ratio DECIMAL(5,2),

    total_loans_taken INT DEFAULT 0,
    active_loans_count INT DEFAULT 0,
    completed_loans_count INT DEFAULT 0,
    defaulted_loans_count INT DEFAULT 0,

    total_loan_amount DECIMAL(15,2) DEFAULT 0.00,
    total_outstanding_loan_amount DECIMAL(15,2) DEFAULT 0.00,

    total_emi_paid INT DEFAULT 0,
    total_emi_missed INT DEFAULT 0,
    late_payment_count INT DEFAULT 0,

    repayment_history_score DECIMAL(5,2),

    risk_category ENUM(
        'LOW',
        'MEDIUM',
        'HIGH'
    ) DEFAULT 'LOW',

    fraud_flag BOOLEAN DEFAULT FALSE,

    last_financial_reviewed_at DATETIME,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);
INSERT INTO customer_financial_profile
(financial_profile_id, customer_id,
credit_score, credit_score_provider, credit_score_updated_at,
total_existing_debt, monthly_emi_obligation,
debt_to_income_ratio,
total_loans_taken, active_loans_count,
completed_loans_count, defaulted_loans_count,
total_loan_amount, total_outstanding_loan_amount,
total_emi_paid, total_emi_missed, late_payment_count,
repayment_history_score, risk_category, fraud_flag,
last_financial_reviewed_at)
VALUES
(6001, 1001,
782, 'CIBIL', '2026-08-01 09:30:00',
0.00, 0.00,
0.00,
0, 0,
0, 0,
0.00, 0.00,
0, 0, 0,
100.00, 'LOW', FALSE,
'2026-08-01 09:35:00'),

(6002, 1002,
756, 'CIBIL', '2026-08-01 10:00:00',
480000.00, 18500.00,
17.62,
2, 1,
1, 0,
850000.00, 480000.00,
34, 0, 1,
94.00, 'LOW', FALSE,
'2026-08-01 10:05:00'),

(6003, 1003,
728, 'CIBIL', '2026-08-02 12:20:00',
0.00, 0.00,
0.00,
1, 0,
1, 0,
600000.00, 0.00,
36, 1, 2,
89.00, 'LOW', FALSE,
'2026-08-02 12:25:00');

CREATE TABLE customer_credentials (
    credential_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL UNIQUE,

    mpin_hash VARCHAR(255) NOT NULL,

    mpin_failed_attempts INT DEFAULT 0,
    mpin_locked_until DATETIME,

    last_mpin_changed_at DATETIME,
    credential_status ENUM(
        'ACTIVE',
        'LOCKED',
        'DISABLED'
    ) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);

CREATE TABLE login_attempts (
    attempt_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT,

    attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    ip_address VARCHAR(45),
    device_id VARCHAR(255),
    user_agent VARCHAR(500),

    attempt_status ENUM(
        'SUCCESS',
        'FAILED',
        'BLOCKED',
        'OTP_REQUIRED',
        'CHALLENGE_REQUIRED'
    ) NOT NULL,

    failure_reason VARCHAR(255),

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);

CREATE TABLE customer_sessions (
    session_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,

    session_token_hash VARCHAR(255) NOT NULL UNIQUE,

    device_id VARCHAR(255),
    device_name VARCHAR(150),

    ip_address VARCHAR(45),
    user_agent VARCHAR(500),

    login_latitude DECIMAL(10,7),
    login_longitude DECIMAL(10,7),
    login_city VARCHAR(100),
    login_country VARCHAR(100),

    login_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity_at DATETIME,
    logout_at DATETIME,

    session_status ENUM(
        'ACTIVE',
        'ENDED',
        'TERMINATED',
        'EXPIRED'
    ) DEFAULT 'ACTIVE',

    termination_reason VARCHAR(255),

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);

CREATE TABLE customer_documents (
    document_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,

    document_type ENUM(
        'SALARY_SLIP',
        'BANK_STATEMENT',
        'FORM_16',
        'ITR',
        'APPOINTMENT_LETTER',
        'EMPLOYEE_ID',
        'PROFESSIONAL_CERTIFICATE',
        'BUSINESS_REGISTRATION',
        'GST_CERTIFICATE',
        'MSME_CERTIFICATE',
        'BALANCE_SHEET',
        'PROFIT_LOSS_STATEMENT',
        'AUDIT_REPORT',
        'GST_RETURN',
        'BUSINESS_BANK_STATEMENT',
        'BUSINESS_CONTINUITY_PROOF',
        'ACADEMIC_MARKSHEET',
        'ADMISSION_LETTER',
        'PASSPORT',
        'VISA',
        'I20_CAS',
        'PENSION_PAYMENT_ORDER',
        'PENSION_SLIP',
        'FD_CERTIFICATE',
        'PROPERTY_DOCUMENT',
        'GOLD_VALUATION',
        'AFFIDAVIT',
        'LAND_RECORD',
        'KCC_RECORD',
        'PLATFORM_EARNING_REPORT',
        'FORM_26AS',
        'OTHER'
    ) NOT NULL,

    document_name VARCHAR(255) NOT NULL,

    file_path VARCHAR(500),
    file_hash VARCHAR(128),

    issue_date DATE,
    expiry_date DATE,

    document_status ENUM(
        'UPLOADED',
        'UNDER_REVIEW',
        'VERIFIED',
        'REJECTED',
        'EXPIRED'
    ) DEFAULT 'UPLOADED',

    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);
INSERT INTO customer_documents
(document_id, customer_id, document_type, document_name,
file_path, file_hash, issue_date, expiry_date,
document_status, uploaded_at)
VALUES
(9001, 1001, 'EMPLOYEE_ID',
'Arjun_Mehta_Employee_ID.pdf',
'/storage/customer-documents/CUST1001/identity/Arjun_Mehta_Employee_ID.pdf',
NULL, '2022-08-01', NULL,
'VERIFIED', '2026-08-05 10:25:00'),

(9002, 1001, 'BANK_STATEMENT',
'Arjun_Mehta_Bank_Statement_Jan-Jun_2026.pdf',
'/storage/customer-documents/CUST1001/income/Arjun_Mehta_Bank_Statement_Jan-Jun_2026.pdf',
NULL, '2026-07-01', NULL,
'VERIFIED', '2026-08-05 10:27:00'),

(9003, 1002, 'SALARY_SLIP',
'Priya_Sharma_Salary_Slips_Jan-Jun_2026.pdf',
'/storage/customer-documents/CUST1002/income/Priya_Sharma_Salary_Slips_Jan-Jun_2026.pdf',
NULL, '2026-06-30', NULL,
'VERIFIED', '2026-08-03 11:00:00'),

(9004, 1002, 'FORM_16',
'Priya_Sharma_Form16_FY2025-26.pdf',
'/storage/customer-documents/CUST1002/income/Priya_Sharma_Form16_FY2025-26.pdf',
NULL, '2026-06-15', NULL,
'VERIFIED', '2026-08-03 11:05:00'),

(9005, 1002, 'BANK_STATEMENT',
'Priya_Sharma_Bank_Statement_Jan-Jun_2026.pdf',
'/storage/customer-documents/CUST1002/income/Priya_Sharma_Bank_Statement_Jan-Jun_2026.pdf',
NULL, '2026-07-01', NULL,
'VERIFIED', '2026-08-03 11:10:00'),

(9006, 1003, 'BUSINESS_REGISTRATION',
'Patil_Electricals_Business_Registration.pdf',
'/storage/customer-documents/CUST1003/business/Patil_Electricals_Business_Registration.pdf',
NULL, '2015-04-01', NULL,
'VERIFIED', '2026-08-08 15:20:00'),

(9007, 1003, 'GST_CERTIFICATE',
'Patil_Electricals_GST_Certificate.pdf',
'/storage/customer-documents/CUST1003/business/Patil_Electricals_GST_Certificate.pdf',
NULL, '2017-07-01', NULL,
'VERIFIED', '2026-08-08 15:25:00'),

(9008, 1003, 'BALANCE_SHEET',
'Patil_Electricals_Balance_Sheet_FY2025-26.pdf',
'/storage/customer-documents/CUST1003/business/Patil_Electricals_Balance_Sheet_FY2025-26.pdf',
NULL, '2026-04-30', NULL,
'VERIFIED', '2026-08-08 15:30:00'),

(9009, 1003, 'BUSINESS_BANK_STATEMENT',
'Patil_Electricals_Bank_Statement_2025-26.pdf',
'/storage/customer-documents/CUST1003/business/Patil_Electricals_Bank_Statement_2025-26.pdf',
NULL, '2026-04-01', NULL,
'VERIFIED', '2026-08-08 15:35:00');

CREATE TABLE customer_loans (
    loan_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    customer_id BIGINT NOT NULL,

    loan_account_number VARCHAR(30) NOT NULL UNIQUE,

    loan_type ENUM(
        'PERSONAL',
        'HOME',
        'EDUCATION',
        'VEHICLE',
        'GOLD',
        'BUSINESS',
        'AGRICULTURE',
        'OTHER'
    ) NOT NULL,

    loan_purpose VARCHAR(255),

    application_date DATE,
    approval_date DATE,
    sanction_date DATE,
    disbursement_date DATE,

    sanctioned_amount DECIMAL(15,2),
    disbursed_amount DECIMAL(15,2),

    interest_rate DECIMAL(5,2),
    interest_type ENUM(
        'FIXED',
        'FLOATING'
    ),

    tenure_months INT,

    emi_amount DECIMAL(15,2),

    processing_fee DECIMAL(15,2),
    insurance_amount DECIMAL(15,2),
    other_charges DECIMAL(15,2),

    total_repayment_amount DECIMAL(15,2),
    total_amount_paid DECIMAL(15,2) DEFAULT 0.00,
    outstanding_principal DECIMAL(15,2) DEFAULT 0.00,
    outstanding_interest DECIMAL(15,2) DEFAULT 0.00,

    loan_start_date DATE,
    expected_end_date DATE,
    actual_end_date DATE,

    total_emi_count INT,
    paid_emi_count INT DEFAULT 0,
    pending_emi_count INT DEFAULT 0,
    missed_emi_count INT DEFAULT 0,
    late_payment_count INT DEFAULT 0,

    collateral_required BOOLEAN DEFAULT FALSE,
    collateral_type VARCHAR(100),
    collateral_value DECIMAL(15,2),

    guarantor_required BOOLEAN DEFAULT FALSE,
    guarantor_name VARCHAR(150),

    loan_status ENUM(
        'PENDING',
        'APPROVED',
        'ACTIVE',
        'CLOSED',
        'REJECTED',
        'DEFAULTED',
        'SETTLED',
        'RESTRUCTURED',
        'CANCELLED'
    ) NOT NULL,

    repayment_status ENUM(
        'CURRENT',
        'OVERDUE',
        'DEFAULTED',
        'COMPLETED'
    ) DEFAULT 'CURRENT',

    days_past_due INT DEFAULT 0,

    last_payment_date DATE,
    next_payment_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);
INSERT INTO customer_loans
(loan_id, customer_id, loan_account_number,
loan_type, loan_purpose,
application_date, approval_date, sanction_date, disbursement_date,
sanctioned_amount, disbursed_amount,
interest_rate, interest_type, tenure_months,
emi_amount,
processing_fee, insurance_amount, other_charges,
total_repayment_amount, total_amount_paid,
outstanding_principal, outstanding_interest,
loan_start_date, expected_end_date, actual_end_date,
total_emi_count, paid_emi_count, pending_emi_count,
missed_emi_count, late_payment_count,
collateral_required, collateral_type, collateral_value,
guarantor_required, guarantor_name,
loan_status, repayment_status, days_past_due,
last_payment_date, next_payment_date)
VALUES
(7001, 1002, 'PL-AEGIS-10020001',
'PERSONAL', 'Home renovation',
'2022-01-10', '2022-01-14', '2022-01-15', '2022-01-17',
500000.00, 500000.00,
11.50, 'FIXED', 36,
16476.00,
5000.00, 2500.00, 500.00,
593136.00, 593136.00,
0.00, 0.00,
'2022-02-01', '2025-01-01', '2025-01-01',
36, 36, 0,
0, 1,
FALSE, NULL, NULL,
FALSE, NULL,
'CLOSED', 'COMPLETED', 0,
'2024-12-01', NULL),

(7002, 1002, 'HL-AEGIS-10020002',
'HOME', 'Residential property purchase',
'2025-03-05', '2025-03-12', '2025-03-14', '2025-03-20',
3500000.00, 3500000.00,
8.40, 'FLOATING', 240,
30280.00,
15000.00, 12000.00, 3000.00,
7267200.00, 740000.00,
480000.00, 16000.00,
'2025-04-01', '2045-04-01', NULL,
240, 24, 216,
0, 0,
TRUE, 'PROPERTY', 5000000.00,
FALSE, NULL,
'ACTIVE', 'CURRENT', 0,
'2026-08-01', '2026-09-01');

INSERT INTO customer_loans
(loan_id, customer_id, loan_account_number,
loan_type, loan_purpose,
application_date, approval_date, sanction_date, disbursement_date,
sanctioned_amount, disbursed_amount,
interest_rate, interest_type, tenure_months,
emi_amount,
processing_fee, insurance_amount, other_charges,
total_repayment_amount, total_amount_paid,
outstanding_principal, outstanding_interest,
loan_start_date, expected_end_date, actual_end_date,
total_emi_count, paid_emi_count, pending_emi_count,
missed_emi_count, late_payment_count,
collateral_required, collateral_type, collateral_value,
guarantor_required, guarantor_name,
loan_status, repayment_status, days_past_due,
last_payment_date, next_payment_date)
VALUES
(7003, 1003, 'BL-AEGIS-10030001',
'BUSINESS', 'Business expansion and equipment purchase',
'2022-05-10', '2022-05-18', '2022-05-20', '2022-05-25',
600000.00, 600000.00,
10.25, 'FLOATING', 36,
19380.00,
6000.00, 3500.00, 1000.00,
697680.00, 697680.00,
0.00, 0.00,
'2022-06-01', '2025-06-01', '2025-06-01',
36, 36, 0,
1, 2,
TRUE, 'BUSINESS_ASSET', 850000.00,
FALSE, NULL,
'CLOSED', 'COMPLETED', 0,
'2025-05-01', NULL);

CREATE TABLE loan_payments (
    payment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    loan_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    payment_reference VARCHAR(50) NOT NULL UNIQUE,
    installment_number INT,
    due_date DATE,
    payment_date DATE,
    principal_amount DECIMAL(15,2),
    interest_amount DECIMAL(15,2),
    penalty_amount DECIMAL(15,2),
    total_amount DECIMAL(15,2),
    payment_method ENUM(
        'AUTO_DEBIT',
        'BANK_TRANSFER',
        'UPI',
        'CASH',
        'CHEQUE',
        'CARD',
        'OTHER'
    ),
    payment_status ENUM(
        'PAID',
        'PARTIALLY_PAID',
        'MISSED',
        'LATE',
        'FAILED',
        'REFUNDED'
    ) NOT NULL,

    days_late INT DEFAULT 0,

    transaction_reference VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (loan_id)
        REFERENCES customer_loans(loan_id),

    FOREIGN KEY (customer_id)
        REFERENCES bank_customers(customer_id)
);
INSERT INTO loan_payments
(payment_id, loan_id, customer_id, payment_reference,
installment_number, due_date, payment_date,
principal_amount, interest_amount, penalty_amount, total_amount,
payment_method, payment_status, days_late, transaction_reference)
VALUES
(8001, 7001, 1002, 'PAY-1002-0001',
1, '2022-03-01', '2022-03-01',
11000.00, 5476.00, 0.00, 16476.00,
'AUTO_DEBIT', 'PAID', 0, 'TXN-AEGIS-10020001'),

(8002, 7001, 1002, 'PAY-1002-0002',
2, '2022-04-01', '2022-04-01',
11100.00, 5376.00, 0.00, 16476.00,
'AUTO_DEBIT', 'PAID', 0, 'TXN-AEGIS-10020002');
