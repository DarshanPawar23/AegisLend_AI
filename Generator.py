import os
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image as ReportLabImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.barcode import code128

# ---------------------------------------------------------
# Shared Design System
# ---------------------------------------------------------
PRIMARY = colors.HexColor("#0F2942")     # Aegis Slate Navy
SECONDARY = colors.HexColor("#1E5F74")   # Deep Corporate Teal
ACCENT = colors.HexColor("#F0F4F8")      # Light Gray Panel
TEXT_DARK = colors.HexColor("#2D3748")   # Charcoal
BORDER_COLOR = colors.HexColor("#CBD5E0")
MUTED = colors.HexColor("#718096")

styles = getSampleStyleSheet()

header_title = ParagraphStyle('HeaderTitle', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=PRIMARY)
header_sub = ParagraphStyle('HeaderSub', fontName='Helvetica', fontSize=8, leading=11, textColor=MUTED)
cell_bold = ParagraphStyle('CellBold', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=TEXT_DARK)
cell_normal = ParagraphStyle('CellNormal', fontName='Helvetica', fontSize=8, leading=10, textColor=TEXT_DARK)
cell_right = ParagraphStyle('CellRight', fontName='Helvetica', fontSize=8, leading=10, alignment=2, textColor=TEXT_DARK)
cell_right_bold = ParagraphStyle('CellRightBold', fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=2, textColor=TEXT_DARK)


def create_vikram_identity_pdf(
    output_filename="storage/customer-documents/CUST1003/identity/Vikram_Patil_Identity.pdf",
    image_path="storage/customer-profiles/vikram.jpeg"
):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    card_w, card_h = 3.375 * inch, 2.125 * inch

    doc = SimpleDocTemplate(output_filename, pagesize=(card_w, card_h), leftMargin=6, rightMargin=6, topMargin=5, bottomMargin=5)
    story = []

    c_company = ParagraphStyle('Comp', fontName='Helvetica-Bold', fontSize=6.5, leading=8, textColor=colors.white, alignment=1)
    c_sub = ParagraphStyle('Sub', fontName='Helvetica', fontSize=4.5, leading=6, textColor=colors.HexColor("#E2E8F0"), alignment=1)
    c_name = ParagraphStyle('Name', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=PRIMARY)
    c_role = ParagraphStyle('Role', fontName='Helvetica-Bold', fontSize=5.5, leading=7, textColor=SECONDARY)
    c_field = ParagraphStyle('Field', fontName='Helvetica', fontSize=4.8, leading=6.5, textColor=TEXT_DARK)

    header_table = Table(
        [[Paragraph("PATIL ELECTRICALS &bull; COMMERCIAL DIVISION", c_company)],
         [Paragraph("Proprietorship Commercial Identity Card", c_sub)]],
        colWidths=[card_w - 12]
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 3))

    img_width, img_height = 0.75 * inch, 0.95 * inch
    resolved_img = None
    for cand in [image_path, "storage/customer-profiles/vikram.jpg", "storage/customer-profiles/CUST1003.jpg"]:
        if os.path.exists(cand):
            resolved_img = cand
            break

    if resolved_img:
        photo_flowable = ReportLabImage(resolved_img, width=img_width, height=img_height)
    else:
        no_img_style = ParagraphStyle('NoImg', fontName='Helvetica', fontSize=5, alignment=1, textColor=MUTED)
        photo_table = Table([[Paragraph("PHOTO<br/>HERE", no_img_style)]], colWidths=[img_width], rowHeights=[img_height])
        photo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E2E8F0")),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        photo_flowable = photo_table

    info_data = [
        [Paragraph("VIKRAM RAJ PATIL", c_name)],
        [Paragraph("Managing Proprietor", c_role)],
        [Spacer(1, 1)],
        [Paragraph("<b>Entity:</b> Patil Electricals", c_field)],
        [Paragraph("<b>Customer ID:</b> CUST1003", c_field)],
        [Paragraph("<b>PAN:</b> CDEFG3456H", c_field)],
        [Paragraph("<b>City:</b> Belagavi | <b>Ph:</b> +91 9000001003", c_field)]
    ]
    info_table = Table(info_data, colWidths=[2.15 * inch])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    body_table = Table([[photo_flowable, info_table]], colWidths=[img_width + 4, 2.2 * inch])
    body_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(body_table)
    story.append(Spacer(1, 3))

    barcode = code128.Code128("CUST1003-ENT", barWidth=0.7, barHeight=10)
    footer_text = ParagraphStyle('SecFoot', fontName='Helvetica', fontSize=3.5, leading=4.5, textColor=MUTED, alignment=1)
    bottom_table = Table([
        [barcode],
        [Paragraph("AegisLend Verified Commercial Identity &bull; Patil Electricals, Tilakwadi, Belagavi", footer_text)]
    ], colWidths=[card_w - 12])
    bottom_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 0.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.5),
    ]))
    story.append(bottom_table)

    doc.build(story)
    print(f"Generated: {output_filename}")


# =========================================================
# 2. BUSINESS REGISTRATION CERTIFICATE (MSME / UDYAM)
# =========================================================
def create_vikram_business_registration_pdf(
    output_filename="storage/customer-documents/CUST1003/business/Patil_Electricals_Business_Registration.pdf"
):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    doc = SimpleDocTemplate(output_filename, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    header_data = [
        [
            Paragraph("<b>GOVERNMENT OF INDIA</b><br/>"
                      "Ministry of Micro, Small and Medium Enterprises<br/>"
                      "UDYAM REGISTRATION CERTIFICATE", ParagraphStyle('HGov', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=PRIMARY))
        ]
    ]
    h_table = Table(header_data, colWidths=[7.4 * inch])
    h_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY),
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(h_table)
    story.append(Spacer(1, 10))

    reg_info = [
        [Paragraph("<b>UDYAM REGISTRATION NUMBER:</b>", cell_bold), Paragraph("<b>UDYAM-KA-06-0049218</b>", cell_bold)],
        [Paragraph("<b>NAME OF ENTERPRISE:</b>", cell_bold), Paragraph("<b>PATIL ELECTRICALS</b>", cell_bold)],
        [Paragraph("<b>PROPRIETOR NAME:</b>", cell_normal), Paragraph("VIKRAM RAJ PATIL", cell_normal)],
        [Paragraph("<b>ORGANIZATION TYPE:</b>", cell_normal), Paragraph("Sole Proprietorship", cell_normal)],
        [Paragraph("<b>MAJOR ACTIVITY:</b>", cell_normal), Paragraph("Trading, Electrical Retail & Industrial Contracting", cell_normal)],
        [Paragraph("<b>ENTERPRISE TYPE:</b>", cell_normal), Paragraph("Small Enterprise", cell_normal)],
        [Paragraph("<b>DATE OF COMMENCEMENT:</b>", cell_normal), Paragraph("01/04/2015", cell_normal)],
        [Paragraph("<b>DATE OF REGISTRATION:</b>", cell_normal), Paragraph("01/04/2015", cell_normal)],
        [Paragraph("<b>OFFICE ADDRESS:</b>", cell_normal),
         Paragraph("42 Market Road, Tilakwadi, Belagavi, Karnataka - 590006", cell_normal)],
        [Paragraph("<b>PAN:</b>", cell_normal), Paragraph("CDEFG3456H", cell_normal)],
        [Paragraph("<b>BANK DETAILS:</b>", cell_normal), Paragraph("Aegis Bank Limited | A/C: AEGIS10010003", cell_normal)],
    ]
    reg_table = Table(reg_info, colWidths=[2.5 * inch, 4.9 * inch])
    reg_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(reg_table)
    story.append(Spacer(1, 15))

    cert_text = (
        "This is to certify that M/s <b>PATIL ELECTRICALS</b> is officially registered as a Small Enterprise "
        "under the Ministry of MSME, Government of India. Verified via National Portal for AegisLend Credit Underwriting."
    )
    story.append(Paragraph(cert_text, ParagraphStyle('CertDesc', fontName='Helvetica', fontSize=8, leading=11, textColor=MUTED, alignment=1)))

    doc.build(story)
    print(f"Generated: {output_filename}")


# =========================================================
# 3. GST REGISTRATION CERTIFICATE (FORM GST REG-06)
# =========================================================
def create_vikram_gst_certificate_pdf(
    output_filename="storage/customer-documents/CUST1003/business/Patil_Electricals_GST_Certificate.pdf"
):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    doc = SimpleDocTemplate(output_filename, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    title_data = [
        [Paragraph("<b>Government of India</b><br/>"
                   "<b>Form GST REG-06</b><br/>"
                   "[See Rule 10(1)]<br/>"
                   "<b>REGISTRATION CERTIFICATE</b>", ParagraphStyle('GSTTitle', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=PRIMARY))]
    ]
    title_table = Table(title_data, colWidths=[7.4 * inch])
    title_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY),
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 10))

    gst_data = [
        [Paragraph("1. GSTIN", cell_bold), Paragraph("<b>29CDEFG3456H1Z5</b>", cell_bold)],
        [Paragraph("2. Legal Name", cell_normal), Paragraph("VIKRAM RAJ PATIL", cell_normal)],
        [Paragraph("3. Trade Name", cell_bold), Paragraph("<b>PATIL ELECTRICALS</b>", cell_bold)],
        [Paragraph("4. Constitution of Business", cell_normal), Paragraph("Proprietorship", cell_normal)],
        [Paragraph("5. Address of Principal Place", cell_normal), Paragraph("42 Market Road, Tilakwadi, Belagavi, Karnataka, 590006", cell_normal)],
        [Paragraph("6. Date of Liability", cell_normal), Paragraph("01/07/2017", cell_normal)],
        [Paragraph("7. Period of Validity", cell_normal), Paragraph("From 01/07/2017 to Regular", cell_normal)],
        [Paragraph("8. Type of Registration", cell_normal), Paragraph("Regular", cell_normal)],
        [Paragraph("9. Jurisdictional Office", cell_normal), Paragraph("Ward-1, Belagavi Commercial Tax Division, Karnataka", cell_normal)],
    ]
    gst_table = Table(gst_data, colWidths=[2.4 * inch, 5.0 * inch])
    gst_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(gst_table)
    story.append(Spacer(1, 15))

    sign_data = [
        [Paragraph("<b>Approved By:</b> Assistant Commissioner of Commercial Taxes<br/>Belagavi Ward-1", cell_normal),
         Paragraph("<b>Date of Issue:</b> 01-Jul-2017<br/><i>Digitally Signed (GSTN System)</i>", ParagraphStyle('SR', parent=cell_normal, alignment=2))]
    ]
    story.append(Table(sign_data, colWidths=[3.7 * inch, 3.7 * inch]))

    doc.build(story)
    print(f"Generated: {output_filename}")


# =========================================================
# 4. BALANCE SHEET (FY 2025-26)
# =========================================================
def create_vikram_balance_sheet_pdf(
    output_filename="storage/customer-documents/CUST1003/business/Patil_Electricals_Balance_Sheet_FY2025-26.pdf"
):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    doc = SimpleDocTemplate(output_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    header = [
        [Paragraph("<b>PATIL ELECTRICALS</b><br/>"
                   "Proprietor: Vikram Raj Patil | PAN: CDEFG3456H<br/>"
                   "42 Market Road, Tilakwadi, Belagavi - 590006<br/>"
                   "<b>BALANCE SHEET AS AT 31ST MARCH, 2026</b>", ParagraphStyle('BSHead', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=PRIMARY))]
    ]
    t_head = Table(header, colWidths=[7.6 * inch])
    t_head.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY),
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_head)
    story.append(Spacer(1, 8))

    bs_data = [
        [Paragraph("<b>LIABILITIES</b>", cell_bold), Paragraph("<b>AMOUNT (INR)</b>", cell_right_bold),
         Paragraph("<b>ASSETS</b>", cell_bold), Paragraph("<b>AMOUNT (INR)</b>", cell_right_bold)],
        [Paragraph("<b>Proprietor's Capital:</b>", cell_bold), Paragraph("", cell_right),
         Paragraph("<b>Fixed Assets:</b>", cell_bold), Paragraph("", cell_right)],
        [Paragraph("Opening Capital Balance", cell_normal), Paragraph("28,40,000.00", cell_right),
         Paragraph("Shop Premises & Showroom", cell_normal), Paragraph("35,00,000.00", cell_right)],
        [Paragraph("Add: Net Profit for FY26", cell_normal), Paragraph("21,60,000.00", cell_right),
         Paragraph("Testing & Installation Equipment", cell_normal), Paragraph("8,50,000.00", cell_right)],
        [Paragraph("Less: Proprietor Drawings", cell_normal), Paragraph("(7,20,000.00)", cell_right),
         Paragraph("Delivery Vans & Vehicles", cell_normal), Paragraph("4,80,000.00", cell_right)],
        [Paragraph("<b>Closing Capital:</b>", cell_bold), Paragraph("<b>42,80,000.00</b>", cell_right_bold),
         Paragraph("Less: Depreciation Reserve", cell_normal), Paragraph("(3,20,000.00)", cell_right)],

        [Paragraph("<b>Current Liabilities:</b>", cell_bold), Paragraph("", cell_right),
         Paragraph("<b>Current Assets:</b>", cell_bold), Paragraph("", cell_right)],
        [Paragraph("Sundry Trade Creditors", cell_normal), Paragraph("14,50,000.00", cell_right),
         Paragraph("Closing Stock / Inventory", cell_normal), Paragraph("18,90,000.00", cell_right)],
        [Paragraph("Advance from Customers", cell_normal), Paragraph("3,20,000.00", cell_right),
         Paragraph("Sundry Debtors (Receivables)", cell_normal), Paragraph("12,40,000.00", cell_right)],
        [Paragraph("Statutory Dues (GST/TDS)", cell_normal), Paragraph("2,60,000.00", cell_right),
         Paragraph("Aegis Bank Current A/C (1003)", cell_normal), Paragraph("6,40,000.00", cell_right)],
        [Paragraph("Outstanding Operational Expenses", cell_normal), Paragraph("80,000.00", cell_right),
         Paragraph("Cash in Hand", cell_normal), Paragraph("1,10,000.00", cell_right)],

        [Paragraph("<b>TOTAL LIABILITIES</b>", cell_bold), Paragraph("<b>63,90,000.00</b>", cell_right_bold),
         Paragraph("<b>TOTAL ASSETS</b>", cell_bold), Paragraph("<b>63,90,000.00</b>", cell_right_bold)],
    ]
    t_bs = Table(bs_data, colWidths=[2.3 * inch, 1.5 * inch, 2.3 * inch, 1.5 * inch])
    t_bs.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('LINEBELOW', (0, -1), (-1, -1), 1.5, PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_bs)
    story.append(Spacer(1, 15))

    sig_data = [
        [Paragraph("<b>For Patil Electricals</b><br/><br/><br/><b>Vikram Raj Patil</b><br/>Proprietor", cell_normal),
         Paragraph("<b>As per our report of even date</b><br/>For S. B. Kulkarni & Associates<br/>Chartered Accountants (FRN: 010293S)<br/><br/><b>CA S. B. Kulkarni</b> (Partner, M.No: 204918)", ParagraphStyle('CASig', parent=cell_normal, alignment=2))]
    ]
    story.append(Table(sig_data, colWidths=[3.8 * inch, 3.8 * inch]))

    doc.build(story)
    print(f"Generated: {output_filename}")


# =========================================================
# 5. PROFIT & LOSS STATEMENT (FY 2025-26)
# =========================================================
def create_vikram_profit_loss_pdf(
    output_filename="storage/customer-documents/CUST1003/business/Patil_Electricals_Profit_Loss_FY2025-26.pdf"
):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    doc = SimpleDocTemplate(output_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    header = [
        [Paragraph("<b>PATIL ELECTRICALS</b><br/>"
                   "42 Market Road, Tilakwadi, Belagavi - 590006<br/>"
                   "<b>STATEMENT OF PROFIT & LOSS FOR THE YEAR ENDED 31ST MARCH, 2026</b>", ParagraphStyle('PLHead', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=PRIMARY))]
    ]
    t_head = Table(header, colWidths=[7.6 * inch])
    t_head.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY),
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_head)
    story.append(Spacer(1, 8))

    pl_data = [
        [Paragraph("<b>PARTICULARS</b>", cell_bold), Paragraph("<b>SCHEDULE</b>", cell_bold), Paragraph("<b>AMOUNT (INR)</b>", cell_right_bold)],
        [Paragraph("<b>I. REVENUE FROM OPERATIONS (Gross Turnover)</b>", cell_bold), Paragraph("1", cell_normal), Paragraph("<b>2,16,00,000.00</b>", cell_right_bold)],
        [Paragraph("II. Other Operational Income", cell_normal), Paragraph("2", cell_normal), Paragraph("2,40,000.00", cell_right)],
        [Paragraph("<b>III. TOTAL REVENUE (I + II)</b>", cell_bold), Paragraph("", cell_normal), Paragraph("<b>2,18,40,000.00</b>", cell_right_bold)],
        [Paragraph("<b>IV. EXPENSES:</b>", cell_bold), Paragraph("", cell_normal), Paragraph("", cell_right)],
        [Paragraph("Cost of Materials Consumed & Traded Goods", cell_normal), Paragraph("3", cell_normal), Paragraph("1,54,00,000.00", cell_right)],
        [Paragraph("Employee Benefits & Technical Staff Wages", cell_normal), Paragraph("4", cell_normal), Paragraph("16,80,000.00", cell_right)],
        [Paragraph("Finance Costs (Bank Charges & Working Capital)", cell_normal), Paragraph("5", cell_normal), Paragraph("1,40,000.00", cell_right)],
        [Paragraph("Depreciation & Amortization Expense", cell_normal), Paragraph("6", cell_normal), Paragraph("3,20,000.00", cell_right)],
        [Paragraph("Showroom Rent, Electricity & Warehouse Overheads", cell_normal), Paragraph("7", cell_normal), Paragraph("14,60,000.00", cell_right)],
        [Paragraph("Administrative, Freight & Marketing Expenses", cell_normal), Paragraph("8", cell_normal), Paragraph("6,80,000.00", cell_right)],
        [Paragraph("<b>TOTAL EXPENSES (IV)</b>", cell_bold), Paragraph("", cell_normal), Paragraph("<b>1,96,80,000.00</b>", cell_right_bold)],
        [Paragraph("<b>V. PROFIT BEFORE TAX (III - IV)</b>", cell_bold), Paragraph("", cell_normal), Paragraph("<b>21,60,000.00</b>", cell_right_bold)],
        [Paragraph("VI. Tax Expense (Income Tax Provisions)", cell_normal), Paragraph("", cell_normal), Paragraph("4,10,000.00", cell_right)],
        [Paragraph("<b>VII. NET PROFIT AFTER TAX FOR THE YEAR</b>", cell_bold), Paragraph("", cell_normal), Paragraph("<b>17,50,000.00</b>", cell_right_bold)],
    ]
    t_pl = Table(pl_data, colWidths=[4.2 * inch, 1.4 * inch, 2.0 * inch])
    t_pl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('LINEBELOW', (0, 3), (-1, 3), 1, PRIMARY),
        ('LINEBELOW', (0, 11), (-1, 11), 1, PRIMARY),
        ('LINEBELOW', (0, -1), (-1, -1), 1.5, PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_pl)
    story.append(Spacer(1, 15))

    sig_data = [
        [Paragraph("<b>For Patil Electricals</b><br/><br/><br/><b>Vikram Raj Patil</b><br/>Proprietor", cell_normal),
         Paragraph("<b>Certified as per Books of Accounts</b><br/>For S. B. Kulkarni & Associates<br/>Chartered Accountants<br/><br/><b>CA S. B. Kulkarni</b> (M.No: 204918)", ParagraphStyle('CAS2', parent=cell_normal, alignment=2))]
    ]
    story.append(Table(sig_data, colWidths=[3.8 * inch, 3.8 * inch]))

    doc.build(story)
    print(f"Generated: {output_filename}")


# =========================================================
# 6. BUSINESS BANK STATEMENT (Jan - Jun 2026)
# =========================================================
def create_vikram_bank_statement_pdf(
    output_filename="storage/customer-documents/CUST1003/business/Patil_Electricals_Bank_Statement_2025-26.pdf"
):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    doc = SimpleDocTemplate(output_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    bank_header = [
        [
            Paragraph("<b>AEGIS BANK LIMITED</b><br/>"
                      "Market Branch, Tilakwadi, Belagavi - 590006<br/>"
                      "IFSC: AEGIS000003 | Branch Code: AGB003", header_sub),
            Paragraph("<b>CURRENT ACCOUNT STATEMENT</b><br/>"
                      "Business Prime Current Account<br/>"
                      "Generated: 01-Jul-2026 11:30:15 IST", ParagraphStyle('BRight', parent=header_sub, alignment=2))
        ]
    ]
    t_head = Table(bank_header, colWidths=[4.0 * inch, 3.6 * inch])
    t_head.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    story.append(t_head)
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=4, spaceAfter=8))

    cust_info = [
        [Paragraph("<b>Account Holder:</b>", cell_bold), Paragraph("PATIL ELECTRICALS (Prop: Vikram Raj Patil)", cell_normal),
         Paragraph("<b>Statement Period:</b>", cell_bold), Paragraph("01-Jan-2026 to 30-Jun-2026", cell_normal)],
        [Paragraph("<b>Account Number:</b>", cell_bold), Paragraph("AEGIS10010003", cell_normal),
         Paragraph("<b>Customer ID:</b>", cell_bold), Paragraph("CUST1003", cell_normal)],
        [Paragraph("<b>Registered Address:</b>", cell_bold),
         Paragraph("42 Market Road, Tilakwadi, Belagavi 590006", cell_normal),
         Paragraph("<b>Account Type:</b>", cell_bold), Paragraph("CURRENT - ACTIVE", cell_normal)],
    ]
    t_cust = Table(cust_info, colWidths=[1.3 * inch, 2.7 * inch, 1.3 * inch, 2.3 * inch])
    t_cust.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_cust)
    story.append(Spacer(1, 8))

    summary_data = [
        [
            Paragraph("<b>Opening Balance:</b> INR 4,12,500.00", cell_normal),
            Paragraph("<b>Total Deposits:</b> INR 1,08,20,000.00", cell_normal),
            Paragraph("<b>Total Withdrawals:</b> INR 1,05,92,500.00", cell_normal),
            Paragraph("<b>Closing Balance:</b> INR 6,40,000.00", cell_bold)
        ]
    ]
    t_sum = Table(summary_data, colWidths=[1.9 * inch, 1.9 * inch, 1.9 * inch, 1.9 * inch])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 8))

    transactions = [
        ["Date", "Description / Reference", "Channel", "Withdrawal (Dr)", "Deposit (Cr)", "Balance"],
        ["01-Jan-2026", "OPENING BALANCE B/F", "SYSTEM", "-", "-", "4,12,500.00"],
        ["08-Jan-2026", "CMS CR/Havells India/Distribution Rebate", "CMS-8910", "-", "4,50,000.00", "8,62,500.00"],
        ["15-Jan-2026", "RTGS DR/Polycab Wires/Raw Material", "RTGS-1192", "6,20,000.00", "-", "2,42,500.00"],
        ["28-Jan-2026", "NEFT CR/Belagavi Builders Consortium/Contract", "NEFT-7811", "-", "12,80,000.00", "15,22,500.00"],

        ["05-Feb-2026", "CHQ WDL/Wages & Field Staff Payroll", "CHQ-4001", "1,40,000.00", "-", "13,82,500.00"],
        ["18-Feb-2026", "RTGS DR/Schneider Electric India/Supplies", "RTGS-2201", "9,80,000.00", "-", "4,02,500.00"],
        ["27-Feb-2026", "UPI QR/Counter Retail Collection Summary", "UPI-Aegis", "-", "8,90,000.00", "12,92,500.00"],

        ["10-Mar-2026", "NEFT DR/Advance Income Tax TaxDept", "NetBanking", "2,10,000.00", "-", "10,82,500.00"],
        ["20-Mar-2026", "CMS CR/Commercial Projects Client Receipt", "CMS-9941", "-", "18,40,000.00", "29,22,500.00"],
        ["31-Mar-2026", "RTGS DR/Vendor Bulk Purchase Clearance", "RTGS-3392", "22,50,000.00", "-", "6,72,500.00"],

        ["12-Apr-2026", "GST TAX PMT/GSTN BELAGAVI DIVISION", "OnlineTax", "1,85,000.00", "-", "4,87,500.00"],
        ["25-Apr-2026", "NEFT CR/Karnataka Infra/Subcontracting", "NEFT-8812", "-", "14,50,000.00", "19,37,500.00"],

        ["15-May-2026", "RTGS DR/Anchor Electricals/Stock", "RTGS-4412", "11,20,000.00", "-", "8,17,500.00"],
        ["30-May-2026", "UPI QR/Counter Retail Collection Summary", "UPI-Aegis", "-", "16,20,000.00", "24,37,500.00"],

        ["10-Jun-2026", "RTGS DR/Commercial Showroom Lease Renovation", "RTGS-5510", "4,50,000.00", "-", "19,87,500.00"],
        ["24-Jun-2026", "RTGS DR/Copper Conductor Bulk Procurement", "RTGS-6612", "13,47,500.00", "-", "6,40,000.00"],
        ["30-Jun-2026", "AEGIS BANK/QUARTERLY CHARGES & AMC", "InternalTxn", "500.00", "-", "6,39,500.00"],
        ["30-Jun-2026", "CASH DEPOSIT/COUNTER CLOSE", "BranchCash", "-", "500.00", "6,40,000.00"]
    ]

    tx_table_data = []
    for r_idx, row in enumerate(transactions):
        row_cells = []
        is_h = (r_idx == 0)
        for c_idx, val in enumerate(row):
            st = (cell_bold if c_idx < 3 else cell_right_bold) if is_h else (cell_normal if c_idx < 3 else cell_right)
            row_cells.append(Paragraph(f"<b>{val}</b>" if is_h else val, st))
        tx_table_data.append(row_cells)

    t_tx = Table(tx_table_data, colWidths=[0.85 * inch, 2.75 * inch, 0.95 * inch, 1.0 * inch, 1.0 * inch, 1.05 * inch], repeatRows=1)
    t_tx.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_tx)

    doc.build(story)
    print(f"Generated: {output_filename}")


# =========================================================
# 7. INCOME TAX RETURN (ITR-V ACKNOWLEDGEMENT AY 2026-27)
# =========================================================
def create_vikram_itr_pdf(
    output_filename="storage/customer-documents/CUST1003/financial/Patil_Electricals_ITR_FY2025-26.pdf"
):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    doc = SimpleDocTemplate(output_filename, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    header = [
        [Paragraph("<b>INDIAN INCOME TAX RETURN ACKNOWLEDGEMENT [ITR-V]</b><br/>"
                   "Assessment Year 2026-27 | Form ITR-3 (Business / Profession)<br/>"
                   "[Filed under Section 139(1) of the Income-tax Act, 1961]", ParagraphStyle('ITRHead', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=PRIMARY))]
    ]
    t_head = Table(header, colWidths=[7.4 * inch])
    t_head.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY),
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_head)
    story.append(Spacer(1, 10))

    itr_personal = [
        [Paragraph("<b>PAN:</b>", cell_bold), Paragraph("CDEFG3456H", cell_normal),
         Paragraph("<b>Status:</b>", cell_bold), Paragraph("Individual / Resident", cell_normal)],
        [Paragraph("<b>Name:</b>", cell_bold), Paragraph("VIKRAM RAJ PATIL", cell_normal),
         Paragraph("<b>Trade Name:</b>", cell_bold), Paragraph("PATIL ELECTRICALS", cell_normal)],
        [Paragraph("<b>Address:</b>", cell_bold), Paragraph("42 Market Road, Tilakwadi, Belagavi, KA - 590006", cell_normal),
         Paragraph("<b>Mobile:</b>", cell_bold), Paragraph("+91 9000001003", cell_normal)],
        [Paragraph("<b>Ack Number:</b>", cell_bold), Paragraph("889102941029381", cell_normal),
         Paragraph("<b>Date of Filing:</b>", cell_bold), Paragraph("28-Jul-2026 16:40:12 IST", cell_normal)],
    ]
    t_pers = Table(itr_personal, colWidths=[1.4 * inch, 2.3 * inch, 1.4 * inch, 2.3 * inch])
    t_pers.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(t_pers)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>COMPUTATION OF INCOME & TAX LIABILITY (IN RUPEES)</b>", ParagraphStyle('CompHead', parent=cell_bold, fontSize=9, textColor=PRIMARY)))
    story.append(Spacer(1, 4))

    itr_comp = [
        [Paragraph("<b>Particulars</b>", cell_bold), Paragraph("<b>Amount (Rs.)</b>", cell_right_bold)],
        [Paragraph("1. Profits and Gains from Business or Profession (Patil Electricals)", cell_normal), Paragraph("21,60,000.00", cell_right)],
        [Paragraph("2. Income from Other Sources (Bank Interest & Rebates)", cell_normal), Paragraph("24,500.00", cell_right)],
        [Paragraph("<b>3. Gross Total Income (1 + 2)</b>", cell_bold), Paragraph("<b>21,84,500.00</b>", cell_right_bold)],
        [Paragraph("4. Deductions under Chapter VI-A (Section 80C, 80D)", cell_normal), Paragraph("1,75,000.00", cell_right)],
        [Paragraph("<b>5. Total Taxable Income (Rounded off)</b>", cell_bold), Paragraph("<b>20,09,500.00</b>", cell_right_bold)],
        [Paragraph("6. Total Tax Payable on Taxable Income", cell_normal), Paragraph("4,15,350.00", cell_right)],
        [Paragraph("7. Health & Education Cess @ 4%", cell_normal), Paragraph("16,614.00", cell_right)],
        [Paragraph("<b>8. Total Tax and Cess Payable</b>", cell_bold), Paragraph("<b>4,31,964.00</b>", cell_right_bold)],
        [Paragraph("9. Less: Advance Tax & Self-Assessment Tax Paid", cell_normal), Paragraph("4,31,964.00", cell_right)],
        [Paragraph("<b>10. Net Tax Payable / Refundable</b>", cell_bold), Paragraph("<b>NIL</b>", cell_right_bold)],
    ]
    t_comp = Table(itr_comp, colWidths=[5.4 * inch, 2.0 * inch])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 15))

    disc_text = (
        "This return has been electronically verified by <b>VIKRAM RAJ PATIL</b> in the capacity of Proprietor "
        "on 28-Jul-2026. This acknowledgement does not require physical submission to CPC Bengaluru."
    )
    story.append(Paragraph(disc_text, ParagraphStyle('ITRDisc', fontName='Helvetica', fontSize=7.5, leading=10, textColor=MUTED, alignment=1)))

    doc.build(story)
    print(f"Generated: {output_filename}")


# =========================================================
# RUNNER BLOCK
# =========================================================
if __name__ == "__main__":
    create_vikram_identity_pdf()
    create_vikram_business_registration_pdf()
    create_vikram_gst_certificate_pdf()
    create_vikram_balance_sheet_pdf()
    create_vikram_profit_loss_pdf()
    create_vikram_bank_statement_pdf()
    create_vikram_itr_pdf()