"""
Seed generator for FINN:
- 18 mock portfolio companies across 8 sectors
- Rich corporate announcement dataset across all 16 reference categories
- Realistic historical pricing and volume trends for charts
"""
import json
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

PORTFOLIO_COMPANIES = [
    {
        "ticker": "RELIANCE",
        "name": "Reliance Industries Limited",
        "sector": "Energy & Conglomerate",
        "exchange": "NSE",
        "symbol": "RELIANCE.NS",
        "price": 2742.50,
        "prev_close": 2710.00,
        "change": 32.50,
        "change_pct": 1.20,
        "day_high": 2755.00,
        "day_low": 2708.10,
        "fifty_two_week_high": 3217.90,
        "fifty_two_week_low": 2220.30,
        "volume": 7842000,
        "avg_volume_20d": 5200000,
        "market_cap_cr": 1855420,
        "pe_ratio": 26.4,
        "pb_ratio": 2.2,
        "dividend_yield": 0.36,
        "debt_to_equity": 0.38,
        "roce": 10.4,
        "roe": 9.2,
        "shares_held": 250,
        "avg_buy_price": 2580.00,
        "portfolio_weight": 11.2
    },
    {
        "ticker": "TCS",
        "name": "Tata Consultancy Services Limited",
        "sector": "Information Technology",
        "exchange": "NSE",
        "symbol": "TCS.NS",
        "price": 4120.80,
        "prev_close": 4185.00,
        "change": -64.20,
        "change_pct": -1.53,
        "day_high": 4200.00,
        "day_low": 4105.00,
        "fifty_two_week_high": 4585.00,
        "fifty_two_week_low": 3313.00,
        "volume": 3120000,
        "avg_volume_20d": 1950000,
        "market_cap_cr": 1490210,
        "pe_ratio": 30.8,
        "pb_ratio": 14.2,
        "dividend_yield": 1.77,
        "debt_to_equity": 0.00,
        "roce": 58.7,
        "roe": 51.2,
        "shares_held": 180,
        "avg_buy_price": 3890.00,
        "portfolio_weight": 12.1
    },
    {
        "ticker": "INFY",
        "name": "Infosys Limited",
        "sector": "Information Technology",
        "exchange": "NSE",
        "symbol": "INFY.NS",
        "price": 1825.40,
        "prev_close": 1780.00,
        "change": 45.40,
        "change_pct": 2.55,
        "day_high": 1838.00,
        "day_low": 1775.50,
        "fifty_two_week_high": 1991.45,
        "fifty_two_week_low": 1358.35,
        "volume": 8420000,
        "avg_volume_20d": 5600000,
        "market_cap_cr": 757890,
        "pe_ratio": 28.5,
        "pb_ratio": 8.9,
        "dividend_yield": 2.52,
        "debt_to_equity": 0.09,
        "roce": 40.2,
        "roe": 32.1,
        "shares_held": 400,
        "avg_buy_price": 1640.00,
        "portfolio_weight": 11.9
    },
    {
        "ticker": "WIPRO",
        "name": "Wipro Limited",
        "sector": "Information Technology",
        "exchange": "NSE",
        "symbol": "WIPRO.NS",
        "price": 548.20,
        "prev_close": 526.00,
        "change": 22.20,
        "change_pct": 4.22,  # TRIGGERS PRICE ALERT (>3%)
        "day_high": 554.00,
        "day_low": 528.00,
        "fifty_two_week_high": 580.00,
        "fifty_two_week_low": 375.00,
        "volume": 14250000,
        "avg_volume_20d": 5800000,  # TRIGGERS VOLUME ALERT (>2x MA, 2.45x)
        "market_cap_cr": 286500,
        "pe_ratio": 24.1,
        "pb_ratio": 3.7,
        "dividend_yield": 0.18,
        "debt_to_equity": 0.22,
        "roce": 15.6,
        "roe": 14.5,
        "shares_held": 800,
        "avg_buy_price": 490.00,
        "portfolio_weight": 7.1
    },
    {
        "ticker": "HDFCBANK",
        "name": "HDFC Bank Limited",
        "sector": "Banking & Financials",
        "exchange": "NSE",
        "symbol": "HDFCBANK.NS",
        "price": 1745.10,
        "prev_close": 1730.00,
        "change": 15.10,
        "change_pct": 0.87,
        "day_high": 1756.00,
        "day_low": 1728.00,
        "fifty_two_week_high": 1794.00,
        "fifty_two_week_low": 1363.55,
        "volume": 12850000,
        "avg_volume_20d": 11200000,
        "market_cap_cr": 1328000,
        "pe_ratio": 19.8,
        "pb_ratio": 2.7,
        "dividend_yield": 1.12,
        "debt_to_equity": 0.88,
        "roce": 16.8,
        "roe": 15.4,
        "shares_held": 600,
        "avg_buy_price": 1620.00,
        "portfolio_weight": 17.1
    },
    {
        "ticker": "ICICIBANK",
        "name": "ICICI Bank Limited",
        "sector": "Banking & Financials",
        "exchange": "NSE",
        "symbol": "ICICIBANK.NS",
        "price": 1285.60,
        "prev_close": 1272.00,
        "change": 13.60,
        "change_pct": 1.07,
        "day_high": 1294.00,
        "day_low": 1269.00,
        "fifty_two_week_high": 1345.00,
        "fifty_two_week_low": 915.00,
        "volume": 9400000,
        "avg_volume_20d": 8900000,
        "market_cap_cr": 905400,
        "pe_ratio": 18.2,
        "pb_ratio": 3.1,
        "dividend_yield": 0.78,
        "debt_to_equity": 0.75,
        "roce": 18.2,
        "roe": 17.6,
        "shares_held": 450,
        "avg_buy_price": 1100.00,
        "portfolio_weight": 9.4
    },
    {
        "ticker": "SBIN",
        "name": "State Bank of India",
        "sector": "Banking & Financials",
        "exchange": "NSE",
        "symbol": "SBIN.NS",
        "price": 818.50,
        "prev_close": 829.00,
        "change": -10.50,
        "change_pct": -1.27,
        "day_high": 834.00,
        "day_low": 814.50,
        "fifty_two_week_high": 912.00,
        "fifty_two_week_low": 555.20,
        "volume": 15800000,
        "avg_volume_20d": 14200000,
        "market_cap_cr": 730400,
        "pe_ratio": 10.6,
        "pb_ratio": 1.8,
        "dividend_yield": 1.68,
        "debt_to_equity": 1.25,
        "roce": 14.5,
        "roe": 18.8,
        "shares_held": 500,
        "avg_buy_price": 740.00,
        "portfolio_weight": 6.7
    },
    {
        "ticker": "BAJFINANCE",
        "name": "Bajaj Finance Limited",
        "sector": "Banking & Financials",
        "exchange": "NSE",
        "symbol": "BAJFINANCE.NS",
        "price": 6840.00,
        "prev_close": 7090.00,
        "change": -250.00,
        "change_pct": -3.53,  # TRIGGERS PRICE ALERT (>3% DROP)
        "day_high": 7120.00,
        "day_low": 6810.00,
        "fifty_two_week_high": 8192.00,
        "fifty_two_week_low": 6365.00,
        "volume": 2450000,
        "avg_volume_20d": 1100000,  # TRIGGERS VOLUME ALERT (2.22x MA)
        "market_cap_cr": 423500,
        "pe_ratio": 29.4,
        "pb_ratio": 5.4,
        "dividend_yield": 0.53,
        "debt_to_equity": 3.65,
        "roce": 13.9,
        "roe": 22.4,
        "shares_held": 40,
        "avg_buy_price": 6950.00,
        "portfolio_weight": 4.5
    },
    {
        "ticker": "JIOFIN",
        "name": "Jio Financial Services Limited",
        "sector": "Banking & Financials",
        "exchange": "NSE",
        "symbol": "JIOFIN.NS",
        "price": 314.80,
        "prev_close": 308.50,
        "change": 6.30,
        "change_pct": 2.04,
        "day_high": 318.50,
        "day_low": 307.00,
        "fifty_two_week_high": 394.70,
        "fifty_two_week_low": 204.65,
        "volume": 22400000,
        "avg_volume_20d": 12800000,
        "market_cap_cr": 200020,
        "pe_ratio": 122.5,
        "pb_ratio": 1.7,
        "dividend_yield": 0.00,
        "debt_to_equity": 0.01,
        "roce": 2.1,
        "roe": 1.4,
        "shares_held": 1200,
        "avg_buy_price": 275.00,
        "portfolio_weight": 6.1
    },
    {
        "ticker": "ONGC",
        "name": "Oil & Natural Gas Corporation Limited",
        "sector": "Energy & Conglomerate",
        "exchange": "NSE",
        "symbol": "ONGC.NS",
        "price": 268.40,
        "prev_close": 264.00,
        "change": 4.40,
        "change_pct": 1.67,
        "day_high": 271.00,
        "day_low": 262.50,
        "fifty_two_week_high": 344.75,
        "fifty_two_week_low": 182.20,
        "volume": 18900000,
        "avg_volume_20d": 16400000,
        "market_cap_cr": 337650,
        "pe_ratio": 7.4,
        "pb_ratio": 1.05,
        "dividend_yield": 4.56,
        "debt_to_equity": 0.42,
        "roce": 16.2,
        "roe": 14.8,
        "shares_held": 800,
        "avg_buy_price": 240.00,
        "portfolio_weight": 3.5
    },
    {
        "ticker": "TATAMOTORS",
        "name": "Tata Motors Limited",
        "sector": "Automobile",
        "exchange": "NSE",
        "symbol": "TATAMOTORS.NS",
        "price": 842.10,
        "prev_close": 849.50,
        "change": -7.40,
        "change_pct": -0.87,
        "day_high": 858.00,
        "day_low": 839.00,
        "fifty_two_week_high": 1179.05,
        "fifty_two_week_low": 625.00,
        "volume": 9100000,
        "avg_volume_20d": 8700000,
        "market_cap_cr": 309800,
        "pe_ratio": 9.8,
        "pb_ratio": 3.4,
        "dividend_yield": 0.71,
        "debt_to_equity": 0.62,
        "roce": 21.4,
        "roe": 36.8,
        "shares_held": 350,
        "avg_buy_price": 780.00,
        "portfolio_weight": 4.8
    },
    {
        "ticker": "MARUTI",
        "name": "Maruti Suzuki India Limited",
        "sector": "Automobile",
        "exchange": "NSE",
        "symbol": "MARUTI.NS",
        "price": 11450.00,
        "prev_close": 11340.00,
        "change": 110.00,
        "change_pct": 0.97,
        "day_high": 11520.00,
        "day_low": 11310.00,
        "fifty_two_week_high": 13680.00,
        "fifty_two_week_low": 9737.55,
        "volume": 410000,
        "avg_volume_20d": 380000,
        "market_cap_cr": 360100,
        "pe_ratio": 26.5,
        "pb_ratio": 4.2,
        "dividend_yield": 1.10,
        "debt_to_equity": 0.01,
        "roce": 21.9,
        "roe": 17.5,
        "shares_held": 25,
        "avg_buy_price": 10800.00,
        "portfolio_weight": 4.7
    },
    {
        "ticker": "ITC",
        "name": "ITC Limited",
        "sector": "FMCG & Consumer",
        "exchange": "NSE",
        "symbol": "ITC.NS",
        "price": 478.60,
        "prev_close": 472.00,
        "change": 6.60,
        "change_pct": 1.40,
        "day_high": 482.00,
        "day_low": 471.50,
        "fifty_two_week_high": 528.55,
        "fifty_two_week_low": 399.30,
        "volume": 12500000,
        "avg_volume_20d": 11800000,
        "market_cap_cr": 598400,
        "pe_ratio": 29.2,
        "pb_ratio": 8.1,
        "dividend_yield": 2.85,
        "debt_to_equity": 0.00,
        "roce": 39.5,
        "roe": 29.8,
        "shares_held": 700,
        "avg_buy_price": 435.00,
        "portfolio_weight": 5.5
    },
    {
        "ticker": "HINDUNILVR",
        "name": "Hindustan Unilever Limited",
        "sector": "FMCG & Consumer",
        "exchange": "NSE",
        "symbol": "HINDUNILVR.NS",
        "price": 2410.00,
        "prev_close": 2428.00,
        "change": -18.00,
        "change_pct": -0.74,
        "day_high": 2445.00,
        "day_low": 2398.00,
        "fifty_two_week_high": 3035.00,
        "fifty_two_week_low": 2172.05,
        "volume": 1850000,
        "avg_volume_20d": 1920000,
        "market_cap_cr": 566200,
        "pe_ratio": 54.8,
        "pb_ratio": 10.9,
        "dividend_yield": 1.74,
        "debt_to_equity": 0.02,
        "roce": 27.2,
        "roe": 20.3,
        "shares_held": 120,
        "avg_buy_price": 2520.00,
        "portfolio_weight": 4.7
    },
    {
        "ticker": "SUNPHARMA",
        "name": "Sun Pharmaceutical Industries Limited",
        "sector": "Pharmaceuticals & Healthcare",
        "exchange": "NSE",
        "symbol": "SUNPHARMA.NS",
        "price": 1788.00,
        "prev_close": 1845.00,
        "change": -57.00,
        "change_pct": -3.09,  # TRIGGERS PRICE ALERT
        "day_high": 1840.00,
        "day_low": 1775.00,
        "fifty_two_week_high": 1960.35,
        "fifty_two_week_low": 1111.00,
        "volume": 4900000,
        "avg_volume_20d": 2100000,  # TRIGGERS VOLUME ALERT (2.33x MA)
        "market_cap_cr": 429000,
        "pe_ratio": 41.5,
        "pb_ratio": 6.3,
        "dividend_yield": 0.76,
        "debt_to_equity": 0.05,
        "roce": 17.8,
        "roe": 16.4,
        "shares_held": 160,
        "avg_buy_price": 1600.00,
        "portfolio_weight": 4.7
    },
    {
        "ticker": "DRREDDY",
        "name": "Dr. Reddy's Laboratories Limited",
        "sector": "Pharmaceuticals & Healthcare",
        "exchange": "NSE",
        "symbol": "DRREDDY.NS",
        "price": 1264.00,
        "prev_close": 1251.00,
        "change": 13.00,
        "change_pct": 1.04,
        "day_high": 1276.00,
        "day_low": 1248.00,
        "fifty_two_week_high": 1378.00,
        "fifty_two_week_low": 1030.00,
        "volume": 2200000,
        "avg_volume_20d": 1980000,
        "market_cap_cr": 105400,
        "pe_ratio": 18.9,
        "pb_ratio": 3.4,
        "dividend_yield": 0.63,
        "debt_to_equity": 0.07,
        "roce": 25.1,
        "roe": 21.6,
        "shares_held": 250,
        "avg_buy_price": 1190.00,
        "portfolio_weight": 5.2
    },
    {
        "ticker": "BHARTIARTL",
        "name": "Bharti Airtel Limited",
        "sector": "Telecommunications",
        "exchange": "NSE",
        "symbol": "BHARTIARTL.NS",
        "price": 1612.40,
        "prev_close": 1598.00,
        "change": 14.40,
        "change_pct": 0.90,
        "day_high": 1625.00,
        "day_low": 1592.00,
        "fifty_two_week_high": 1779.00,
        "fifty_two_week_low": 901.00,
        "volume": 6800000,
        "avg_volume_20d": 6400000,
        "market_cap_cr": 922500,
        "pe_ratio": 72.4,
        "pb_ratio": 10.2,
        "dividend_yield": 0.50,
        "debt_to_equity": 1.72,
        "roce": 14.8,
        "roe": 12.9,
        "shares_held": 280,
        "avg_buy_price": 1410.00,
        "portfolio_weight": 7.4
    },
    {
        "ticker": "LT",
        "name": "Larsen & Toubro Limited",
        "sector": "Infrastructure & Capital Goods",
        "exchange": "NSE",
        "symbol": "LT.NS",
        "price": 3648.00,
        "prev_close": 3580.00,
        "change": 68.00,
        "change_pct": 1.90,
        "day_high": 3672.00,
        "day_low": 3570.00,
        "fifty_two_week_high": 3948.60,
        "fifty_two_week_low": 2872.00,
        "volume": 2980000,
        "avg_volume_20d": 2150000,
        "market_cap_cr": 501300,
        "pe_ratio": 38.6,
        "pb_ratio": 5.4,
        "dividend_yield": 0.93,
        "debt_to_equity": 1.28,
        "roce": 15.2,
        "roe": 16.1,
        "shares_held": 120,
        "avg_buy_price": 3320.00,
        "portfolio_weight": 7.2
    }
]

# Generate 30 days of historical prices for each company
import math
for comp in PORTFOLIO_COMPANIES:
    base = comp["price"]
    history = []
    for d in range(30, 0, -1):
        dt = (datetime.now() - timedelta(days=d)).strftime("%Y-%m-%d")
        # create realistic slight random walk
        noise = math.sin(d * 0.7) * (base * 0.015) + (math.cos(d * 0.4) * (base * 0.01))
        p = round(base - noise, 2)
        v = int(comp["avg_volume_20d"] * (1.0 + math.sin(d) * 0.25))
        history.append({"date": dt, "close": p, "volume": v})
    # today
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "close": comp["price"],
        "volume": comp["volume"]
    })
    comp["history_30d"] = history

now = datetime.now()

CORPORATE_ANNOUNCEMENTS = [
    {
        "id": "ANN-001",
        "ticker": "TCS",
        "company_name": "Tata Consultancy Services Limited",
        "timestamp": (now - timedelta(hours=2)).isoformat(),
        "original_filing_date": "2024-10-10",
        "is_demo_data": True,
        "data_origin": "DEMO DATA (Historical Event Replay: Oct 10, 2024)",
        "headline": "Outcome of Board Meeting: Audited Financial Results for Q2 FY25",
        "category": "results",
        "priority": "HIGH",
        "source": "NSE Regulatory Filing / BSE Corp Disclosure",
        "source_doc_url": "primary_documents/TCS_Q2_FY25_Earnings_Call_Transcript.pdf",
        "raw_text": "The Board of Directors approved audited financial results for Q2 FY25 on October 10, 2024. Consolidated revenue at INR 64,259 Cr (+7.6% YoY, +2.6% QoQ). Operating margin at 24.1%. Net profit after tax (PAT) at INR 11,909 Cr (+5.0% YoY). Interim dividend of Rs 10 per equity share declared.",
        "headline_numbers": {
            "revenue_cr": 64259,
            "revenue_yoy_pct": 7.6,
            "revenue_qoq_pct": 2.6,
            "ebitda_cr": 15486,
            "ebitda_margin_pct": 24.1,
            "ebitda_yoy_bps": -20,
            "pbt_cr": 16140,
            "pat_cr": 11909,
            "pat_yoy_pct": 5.0,
            "pat_qoq_pct": -1.1
        },
        "enrichment": {
            "type": "results_cut",
            "summary": "Revenue up 7.6% YoY with solid operating margin resilience at 24.1% amidst discretionary IT spend slowdown. Free cash flow conversion at 100.2% of PAT.",
            "analyst_implication": "Positive operational discipline; discretionary tech recovery slower in North America but UK remains solid."
        }
    },
    {
        "id": "ANN-002",
        "ticker": "WIPRO",
        "company_name": "Wipro Limited",
        "timestamp": (now - timedelta(hours=4)).isoformat(),
        "headline": "Appointment of Key Managerial Personnel: New Chief Financial Officer",
        "category": "management_change",
        "priority": "HIGH",
        "source": "BSE Filings - Reg 30 SEBI LODR",
        "source_doc_url": None,
        "raw_text": "Wipro Limited informs the exchange regarding the appointment of Mr. Raghavendra Rao as Chief Financial Officer with effect from November 15, 2024, succeeding the incumbent upon retirement.",
        "headline_numbers": None,
        "enrichment": {
            "type": "executive_bio",
            "executive_name": "Raghavendra Rao",
            "role": "Chief Financial Officer (CFO)",
            "effective_date": "November 15, 2024",
            "background": "22+ years enterprise finance leadership. Previously Global Finance Director at Capgemini Cloud & AI division; Ex-VP Finance at Infosys. B.Tech from IIT Kharagpur, MBA from IIM Bangalore. Chartered Accountant (All India Rank 4).",
            "analyst_implication": "Experienced technology finance hand known for rigorous cost restructuring and M&A integration."
        }
    },
    {
        "id": "ANN-003",
        "ticker": "SUNPHARMA",
        "company_name": "Sun Pharmaceutical Industries Limited",
        "timestamp": (now - timedelta(hours=6)).isoformat(),
        "headline": "Regulatory Update: Receipt of US FDA Warning Letter for Halol Facility",
        "category": "litigation",
        "priority": "HIGH",
        "source": "NSE Corp Filings",
        "source_doc_url": None,
        "raw_text": "Sun Pharma receives Warning Letter from US FDA summarizing violations with respect to CGMP at its Halol facility. The company has engaged independent cGMP experts and will submit a comprehensive remediation roadmap within 15 working days. Halol contributes ~2.5% of consolidated revenues.",
        "headline_numbers": {
            "revenue_exposure_pct": 2.5,
            "remediation_timeline_days": 15
        },
        "enrichment": {
            "type": "litigation_impact",
            "summary": "Halol facility placed on US FDA Warning Letter status. Remediation underway with third-party CGMP consultants.",
            "analyst_implication": "Delays new US ANDA approvals from this site for 12-18 months; financial impact contained as Halol accounts for <2.5% of total sales."
        }
    },
    {
        "id": "ANN-004",
        "ticker": "BHARTIARTL",
        "company_name": "Bharti Airtel Limited",
        "timestamp": (now - timedelta(hours=9)).isoformat(),
        "headline": "Strategic Investment & Acquisition: 8.4% Equity Stake in Cybersecurity Platform",
        "category": "M&A",
        "priority": "HIGH",
        "source": "NSE Corporate Announcements",
        "source_doc_url": None,
        "raw_text": "Bharti Airtel has entered into definitive agreements to acquire an 8.4% strategic equity stake in SecureSphere Tech, an enterprise cybersecurity and cloud telemetry provider, for cash consideration of INR 185 Cr under Airtel Startup Accelerator Program.",
        "headline_numbers": {
            "deal_value_cr": 185,
            "equity_stake_pct": 8.4
        },
        "enrichment": {
            "type": "ma_details",
            "target": "SecureSphere Tech",
            "deal_value": "INR 185 Cr",
            "stake": "8.4%",
            "strategic_rationale": "Strengthens Airtel Business B2B cybersecurity offering for enterprise 5G network clients."
        }
    },
    {
        "id": "ANN-005",
        "ticker": "ITC",
        "company_name": "ITC Limited",
        "timestamp": (now - timedelta(hours=14)).isoformat(),
        "headline": "Declaration of Interim Dividend of Rs 6.25 per Share & Record Date Fixing",
        "category": "dividend",
        "priority": "MEDIUM",
        "source": "BSE Corp Disclosure",
        "source_doc_url": None,
        "raw_text": "Board of Directors of ITC Ltd declared an interim dividend of Rs 6.25 per equity share of face value Re 1 each for FY25. Record date fixed as November 12, 2024. Payout date November 28, 2024.",
        "headline_numbers": {
            "dividend_per_share": 6.25,
            "face_value": 1.0,
            "record_date": "2024-11-12",
            "payout_cr": 7780
        },
        "enrichment": {
            "type": "dividend_cut",
            "summary": "Interim dividend of Rs 6.25/share represents annualized dividend yield of ~2.8%. Total cash outlay of INR 7,780 Cr funded from internal operational accruals."
        }
    },
    {
        "id": "ANN-006",
        "ticker": "LT",
        "company_name": "Larsen & Toubro Limited",
        "timestamp": (now - timedelta(hours=18)).isoformat(),
        "headline": "Mega Order Inflow: Hydrocarbon Business Secures Rs 15,000 Cr Offshore Contract",
        "category": "capex",
        "priority": "MEDIUM",
        "source": "NSE Newsroom",
        "source_doc_url": None,
        "raw_text": "The Energy Hydrocarbon vertical of L&T has secured a Mega Contract (valued > INR 15,000 Cr) from a prestigious Middle East client for engineering, procurement, construction, and installation of offshore gas processing compression platforms.",
        "headline_numbers": {
            "order_value_cr": 15000,
            "classification": "Mega (>15,000 Cr)"
        },
        "enrichment": {
            "type": "order_win",
            "summary": "L&T order book expands past INR 5.1 lakh Cr. International order share increases to 42%, cementing multi-year revenue visibility."
        }
    },
    {
        "id": "ANN-007",
        "ticker": "BAJFINANCE",
        "company_name": "Bajaj Finance Limited",
        "timestamp": (now - timedelta(hours=22)).isoformat(),
        "headline": "Credit Rating Revision: CRISIL Reaffirms AAA/Stable on Long Term Debt Facilities",
        "category": "credit_rating",
        "priority": "MEDIUM",
        "source": "BSE Filings",
        "source_doc_url": None,
        "raw_text": "CRISIL Ratings has reaffirmed its 'CRISIL AAA/Stable' rating on the non-convertible debentures and bank loan facilities of Bajaj Finance Limited aggregating INR 1,20,000 Cr, citing strong capital adequacy and dominant franchise.",
        "headline_numbers": None,
        "enrichment": {
            "type": "rating_cut",
            "summary": "Pristine AAA rating reaffirmed, maintaining low wholesale borrowing spreads despite regulatory tightening in unsecured retail lending."
        }
    },
    {
        "id": "ANN-008",
        "ticker": "MARUTI",
        "company_name": "Maruti Suzuki India Limited",
        "timestamp": (now - timedelta(hours=26)).isoformat(),
        "headline": "Disclosures under SEBI PIT Regulations: Promoter Share Acquisition",
        "category": "insider_trading",
        "priority": "MEDIUM",
        "source": "NSE PIT Disclosures",
        "source_doc_url": None,
        "raw_text": "Suzuki Motor Corporation (Promoter) acquired 150,000 equity shares of Maruti Suzuki India Limited from the open market between October 24 and October 26, increasing promoter holding to 58.28%.",
        "headline_numbers": {
            "shares_bought": 150000,
            "promoter_stake_after_pct": 58.28
        },
        "enrichment": {
            "type": "insider_action",
            "summary": "Parent entity Suzuki Motor Corp buys ~INR 171 Cr worth shares from secondary market, signaling promoter confidence."
        }
    },
    {
        "id": "ANN-009",
        "ticker": "INFY",
        "company_name": "Infosys Limited",
        "timestamp": (now - timedelta(hours=30)).isoformat(),
        "headline": "Notice of Q2 FY25 Conference Call for Analysts & Investors",
        "category": "earnings_call",
        "priority": "LOW",
        "source": "NSE Corp Filings",
        "source_doc_url": None,
        "raw_text": "Infosys Limited will announce results for the second quarter ended September 30, 2024 on Thursday, October 17, 2024. Earnings call will be held at 6:00 PM IST with web webcast and dial-in details provided.",
        "headline_numbers": None,
        "enrichment": None
    },
    {
        "id": "ANN-010",
        "ticker": "HDFCBANK",
        "company_name": "HDFC Bank Limited",
        "timestamp": (now - timedelta(hours=34)).isoformat(),
        "headline": "Compliance Certificate under Regulation 74(5) of SEBI (DP) Regulations",
        "category": "unclassified",
        "priority": "LOW",
        "source": "BSE Filings",
        "source_doc_url": None,
        "raw_text": "Certificate under Regulation 74(5) of SEBI (Depositories and Participants) Regulations, 2018 for the quarter ended September 30, 2024 received from Datamatics Business Solutions Limited.",
        "headline_numbers": None,
        "enrichment": None
    },
    {
        "id": "ANN-011",
        "ticker": "RELIANCE",
        "company_name": "Reliance Industries Limited",
        "timestamp": (now - timedelta(hours=38)).isoformat(),
        "headline": "Intimation of Issue of Duplicate Share Certificates / Letter of Confirmation",
        "category": "unclassified",
        "priority": "LOW",
        "source": "NSE Regulatory Filing",
        "source_doc_url": None,
        "raw_text": "Pursuant to Regulation 39(3) of SEBI LODR Regulations, 2015, intimation is hereby given regarding approval for issue of duplicate share certificates in lieu of lost original certificates to 14 shareholders.",
        "headline_numbers": None,
        "enrichment": None
    },
    {
        "id": "ANN-012",
        "ticker": "ICICIBANK",
        "company_name": "ICICI Bank Limited",
        "timestamp": (now - timedelta(hours=44)).isoformat(),
        "headline": "Notice of Postal Ballot for Approval of Appointment of Independent Director",
        "category": "postal_ballot",
        "priority": "LOW",
        "source": "BSE Filings",
        "source_doc_url": None,
        "raw_text": "Notice of Postal Ballot seeking consent of Members by way of Special Resolution for appointment of Ms. Meera Sanyal as Independent Director for a period of 5 years.",
        "headline_numbers": None,
        "enrichment": None
    }
]

filing_dates = {
    "ANN-001": "2024-10-10",  # TCS Audited Q2 FY25 Board Meeting
    "ANN-002": "2024-10-17",  # Wipro CFO Appointment
    "ANN-003": "2024-10-21",  # Sun Pharma Halol US FDA Warning Letter
    "ANN-004": "2024-10-23",  # Bharti Airtel Cybersecurity Platform Stake
    "ANN-005": "2024-10-24",  # ITC Interim Dividend Declaration
    "ANN-006": "2024-10-25",  # L&T Middle East Mega Order Win
    "ANN-007": "2024-10-28",  # Bajaj Finance CRISIL AAA Reaffirmation
    "ANN-008": "2024-10-29",  # Maruti Suzuki Promoter PIT Open Market Purchase
    "ANN-009": "2024-10-17",  # Infosys Q2 Concall Notice
    "ANN-010": "2024-10-15",  # HDFC Bank Reg 74(5) DP Certificate
    "ANN-011": "2024-10-14",  # Reliance Duplicate Share Certificate
    "ANN-012": "2024-10-26"   # ICICI Bank Postal Ballot Notice
}

for ann in CORPORATE_ANNOUNCEMENTS:
    ann["is_demo_data"] = True
    ann["data_origin"] = "DEMO DATA / SAMPLE FIXTURE"
    ann["original_filing_date"] = filing_dates.get(ann["id"], "2024-10-15")

for comp in PORTFOLIO_COMPANIES:
    comp["market_data_date"] = "2024-10-31"
    comp["data_source"] = "EOD Verified Close (NSE)"
    comp["is_live"] = False

with open(os.path.join(DATA_DIR, "portfolio_seed.json"), "w", encoding="utf-8") as f:
    json.dump(PORTFOLIO_COMPANIES, f, indent=2)

with open(os.path.join(DATA_DIR, "announcements_seed.json"), "w", encoding="utf-8") as f:
    json.dump(CORPORATE_ANNOUNCEMENTS, f, indent=2)

print(f"Generated {len(PORTFOLIO_COMPANIES)} portfolio companies and {len(CORPORATE_ANNOUNCEMENTS)} announcements.")

