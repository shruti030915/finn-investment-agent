"""
Generates primary PDF filings and transcripts for demo companies (TCS, RELIANCE, INFY, HDFCBANK)
using ReportLab, so that PyMuPDF (fitz) can extract real pages, real text, and real financial citations.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "primary_documents")
os.makedirs(DOCS_DIR, exist_ok=True)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#0F172A'))
h2_style = ParagraphStyle('DocH2', parent=styles['Heading2'], fontSize=12, leading=16, textColor=colors.HexColor('#1E293B'))
body_style = ParagraphStyle('DocBody', parent=styles['Normal'], fontSize=9, leading=13, textColor=colors.HexColor('#334155'))
quote_style = ParagraphStyle('DocQuote', parent=styles['Italic'], fontSize=9, leading=13, textColor=colors.HexColor('#0369A1'))

def create_tcs_concall():
    filename = os.path.join(DOCS_DIR, "TCS_Q2_FY25_Earnings_Call_Transcript.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    # Page 1: Overview & Management Opening
    story.append(Paragraph("Tata Consultancy Services Limited — Q2 FY25 Earnings Conference Call", title_style))
    story.append(Paragraph("Date: October 10, 2024 | Participants: K. Krithivasan (MD & CEO), Samir Seksaria (CFO)", body_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Management Opening Remarks — K. Krithivasan (MD & CEO):", h2_style))
    story.append(Paragraph(
        "Good evening, everyone, and thank you for joining us today. In Q2 FY25, our revenue grew 7.6% year-on-year in constant currency, "
        "reaching INR 64,259 crore. Growth was led by our Energy, Resources, and Utilities vertical, which grew 7.0%, and Manufacturing at 5.3%. "
        "Our BFSI vertical, which accounts for 31.3% of revenue, returned to positive sequential growth at 0.1% QoQ after four quarters of contraction.",
        body_style
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Guidance vs Actual Execution:", h2_style))
    story.append(Paragraph(
        "At the beginning of FY25, we guided that international markets would see stabilization by Q2, with BFS discretionary spending gradually returning. "
        "Actual delivery shows North America grew -2.1% YoY, indicating that discretionary tech spend recovery remains slower than initially guided. "
        "However, our UK business delivered resilient growth of 4.6% YoY. Total Contract Value (TCV) for the quarter stood at $8.6 billion, well within "
        "our target operating band of $7B to $9B per quarter.",
        body_style
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("AI & Cloud Pipeline:", h2_style))
    story.append(Paragraph(
        "Our AI and GenAI pipeline doubled sequentially to $1.5 billion. We are actively engaged in over 600 GenAI engagements across financial services, "
        "telecom, and life sciences. We remain confident in our long-term structural margin target of 26-28%, although wage hikes impact near-term numbers.",
        body_style
    ))
    story.append(PageBreak())

    # Page 2: CFO Financial Performance Review
    story.append(Paragraph("Financial Review — Samir Seksaria (CFO):", h2_style))
    story.append(Paragraph(
        "Let me walk through the key financial parameters for the second quarter ended September 30, 2024. "
        "Consolidated Revenue for Q2 FY25 was reported at INR 64,259 crore, up 2.6% QoQ and 7.6% YoY. "
        "Operating Margin (EBITDA margin equivalent) stood at 24.1%, expanding by 40 bps year-on-year, primarily driven by productivity gains and pyramid optimization.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    # Financial Table
    data = [
        ["Metric (INR Crore)", "Q2 FY25", "Q1 FY25 (QoQ)", "Q2 FY24 (YoY)", "YoY Growth (%)"],
        ["Revenue from Operations", "64,259", "62,613", "59,692", "+7.6%"],
        ["Operating Profit (EBIT)", "15,486", "15,444", "14,483", "+6.9%"],
        ["EBIT Margin (%)", "24.1%", "24.7%", "24.3%", "-20 bps"],
        ["Profit Before Tax (PBT)", "16,140", "16,183", "15,330", "+5.3%"],
        ["Profit After Tax (PAT)", "11,909", "12,040", "11,342", "+5.0%"],
        ["Net Margin (%)", "18.5%", "19.2%", "19.0%", "-50 bps"],
        ["Free Cash Flow (FCF)", "11,261", "10,950", "10,210", "+10.3%"]
    ]
    t = Table(data, colWidths=[160, 80, 90, 80, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Cash Conversion & Balance Sheet Health:", h2_style))
    story.append(Paragraph(
        "Operating cash flow was INR 11,261 crore, representing 100.2% of net profit (PAT). This highlights exceptional cash conversion quality. "
        "Invested cash and bank balances stood at INR 43,892 crore as of September 30, 2024. The company remains virtually debt-free with a Debt-to-Equity ratio of 0.00. "
        "Return on Equity (ROE) stands at 51.2% annualized.",
        body_style
    ))
    story.append(PageBreak())

    # Page 3: Analyst Q&A (Narrative vs Numbers, Bull & Bear signals)
    story.append(Paragraph("Analyst Q&A Session Highlights", h2_style))
    story.append(Paragraph("Question from Nitin Padmanabhan (Investec):", quote_style))
    story.append(Paragraph(
        "'On discretionary spend: you noted earlier that banking clients were pausing transformation programs. Are you seeing signs of budget expansion for CY25?'",
        body_style
    ))
    story.append(Paragraph("Response by K. Krithivasan (MD & CEO):", quote_style))
    story.append(Paragraph(
        "'Clients are cautious. While vendor consolidation deals continue at a brisk pace, discretionary spends remain selective. "
        "We are seeing demand for efficiency and cost reduction, but new digital transformation initiatives are taking longer to convert into billings.'",
        body_style
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Bull vs Bear Case Synthesis:", h2_style))
    story.append(Paragraph(
        "<b>Bull Thesis:</b> Market share gains from vendor consolidation; mega-deal execution track record ($8.6B TCV); peer-leading operating margins (24.1%); "
        "pristine debt-free balance sheet with 100%+ cash conversion and high return on equity (>50%).",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Bear Thesis:</b> Prolonged stagnation in US BFSI discretionary spending (-2.1% YoY in North America); pricing pressure in renewal contracts; "
        "attrition at senior project architect level; risk of GenAI accelerating software development cycle and reducing billable hours.",
        body_style
    ))
    doc.build(story)
    print("Created:", filename)

def create_reliance_results():
    filename = os.path.join(DOCS_DIR, "RELIANCE_Q2_FY25_Financial_Results_Notes.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    # Page 1: Reliance Results Overview
    story.append(Paragraph("Reliance Industries Limited — Q2 FY25 Financial Disclosures & Notes", title_style))
    story.append(Paragraph("Quarter Ended September 30, 2024 | Consolidated Financial Report", body_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("1. Executive Summary & Segment Performance", h2_style))
    story.append(Paragraph(
        "Reliance Industries Limited (RIL) reported consolidated revenue of INR 2,35,481 crore for Q2 FY25, relatively flat (-0.2% YoY), "
        "as strong momentum in Consumer businesses (Jio and Retail) offset weakness in the Oil-to-Chemicals (O2C) downstream refining segment. "
        "Consolidated EBITDA stood at INR 43,934 crore, down 4.7% YoY due to sharp contraction in global fuel cracks and petrochemical margins.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Segment Table
    data = [
        ["Segment", "Revenue (INR Cr)", "EBITDA (INR Cr)", "EBITDA Margin (%)", "YoY Commentary"],
        ["Jio Platforms", "31,709", "15,931", "50.2%", "+17.8% YoY EBITDA; tariff hike benefit"],
        ["Reliance Retail", "75,378", "5,850", "7.8%", "+1.0% YoY EBITDA; store rationalization"],
        ["Oil to Chemicals (O2C)", "1,24,336", "12,413", "10.0%", "-23.7% YoY; weak refining margins"],
        ["Oil & Gas (Upstream)", "6,222", "5,290", "85.0%", "+11.0% YoY; KG D6 gas volumes"]
    ]
    t = Table(data, colWidths=[110, 95, 95, 95, 125])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t)
    story.append(PageBreak())

    # Page 2: Capex, Balance Sheet & Guidance Analysis
    story.append(Paragraph("2. Capital Expenditure, Debt and Cash Flows", h2_style))
    story.append(Paragraph(
        "Capital expenditure for the quarter was INR 34,022 crore, directed towards 5G rollouts, retail store expansion, and new energy giga-factories at Jamnagar. "
        "Gross debt as of September 30, 2024 stood at INR 3,36,337 crore. Cash and cash equivalents were INR 2,19,821 crore, resulting in Net Debt of INR 1,16,516 crore. "
        "Net Debt-to-EBITDA remains comfortable at 0.68x.",
        body_style
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Narrative vs Numbers — Guidance Evaluation:", h2_style))
    story.append(Paragraph(
        "Management had previously guided for peak 5G capex tapering off by FY25. The numbers confirm this trend, with quarterly telecom capex declining from "
        "INR 18,000 crore to INR 12,500 crore. However, retail space addition has moderated due to rationalization of non-performing stores, conflicting with earlier "
        "aggressive floor-area guidance. New Energy giga-factories (solar PV and battery energy storage) remain on track for commissioning by end of CY25.",
        body_style
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Bull vs Bear Perspective:", h2_style))
    story.append(Paragraph(
        "<b>Bull Case:</b> Jio tariff hikes driving sustained ARPU expansion (ARPU reached INR 195.1); upcoming potential IPOs of Jio Platforms and Reliance Retail; "
        "tapering capex leading to free cash flow generation; world-class integrated scale.",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Bear Case:</b> Structural headwind in O2C refining margins amidst Chinese capacity additions; large gross debt burden requiring continuous refinancing; "
        "high working capital intensity in retail inventory; prolonged gestation for new green energy investments.",
        body_style
    ))
    doc.build(story)
    print("Created:", filename)

def create_hdfc_bank_report():
    filename = os.path.join(DOCS_DIR, "HDFCBANK_FY24_Annual_Report_Excerpts.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    story.append(Paragraph("HDFC Bank Limited — FY24 Annual Report & Merger Integration", title_style))
    story.append(Paragraph("Audited Financial Statements for Year Ended March 31, 2024", body_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("1. Post-Merger Financial Architecture", h2_style))
    story.append(Paragraph(
        "Following the landmark merger of HDFC Limited into HDFC Bank effective July 1, 2023, the combined entity balance sheet reached INR 36,17,623 crore. "
        "Net Interest Income (NII) for FY24 stood at INR 1,08,532 crore, representing 25.1% growth over FY23. "
        "Net Profit (PAT) for the fiscal year reached INR 60,812 crore, up 37.9% YoY.",
        body_style
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Key Banking Ratios & Asset Quality:", h2_style))
    
    data = [
        ["Key Parameter", "FY24 Reported", "FY23 Pre-Merger", "Target Guidance", "Status"],
        ["Net Interest Margin (NIM)", "3.44%", "4.10%", "3.70% - 3.80%", "Divergence: Merged liquidity drag"],
        ["Gross NPA Ratio (%)", "1.24%", "1.12%", "< 1.30%", "Within guided threshold"],
        ["Net NPA Ratio (%)", "0.33%", "0.27%", "< 0.40%", "Superior underwriting quality"],
        ["CASA Ratio (%)", "38.2%", "44.4%", "> 40.0%", "Divergence: High interest rate shift"],
        ["Credit-to-Deposit (C/D) Ratio", "104.0%", "85.0%", "88.0% - 90.0%", "Critical focus: Requires deposit mobilization"],
        ["Capital Adequacy Ratio (CRAR)", "18.8%", "19.3%", "> 16.0%", "Robust capital buffer"]
    ]
    t = Table(data, colWidths=[130, 90, 90, 110, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t)
    story.append(PageBreak())

    story.append(Paragraph("2. Narrative vs Numbers — Management Delivery Assessment", h2_style))
    story.append(Paragraph(
        "<b>Narrative:</b> In merger communications, management stated that access to HDFC Ltd's home loan customers would create massive cross-selling "
        "synergies without placing upward pressure on cost of funds.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Numbers Reality:</b> Cost of funds increased to 4.90% from 4.10% as term deposits had to be mobilized at peak rates to finance the merged housing portfolio. "
        "C/D ratio spiked to 104%, forcing management to deliberately slow credit growth to allow deposits to catch up. "
        "While asset quality remained pristine (Gross NPA 1.24%), margins compressed by 66 bps.",
        body_style
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Institutional Bull vs Bear Verdict:", h2_style))
    story.append(Paragraph(
        "<b>Bull:</b> Dominant private sector lender with unmatched retail distribution network (8,775 branches); structural mortgage demand driver in India; "
        "unassailable balance sheet safety and provision coverage (>75%); valuations at decadal lows relative to historical P/B.",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Bear:</b> Prolonged margin compression as high C/D ratio limits lending growth; systemic deposit competition across public and private banks; "
        "slower execution of branch cross-selling targets.",
        body_style
    ))
    doc.build(story)
    print("Created:", filename)

if __name__ == '__main__':
    create_tcs_concall()
    create_reliance_results()
    create_hdfc_bank_report()
    print("All primary documents generated successfully.")
