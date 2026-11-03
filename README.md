# FINN — Financial Investment Intelligence Agent
### Developed for the ENAM Holdings AI Engineer Build Challenge

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.22+-orange.svg)](https://pymupdf.readthedocs.io/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Dark%20Terminal-0F172A.svg)](https://tailwindcss.com)
[![Architecture](https://img.shields.io/badge/Architecture-Push%20%2B%20Pull%20RAG-indigo.svg)]()

FINN is a modern, mobile-first financial intelligence application engineered for public-market investment analysts and fund managers at ENAM Holdings. Designed with the calm simplicity of Linear and Notion and the analytical depth of institutional investment platforms, FINN operates as an autonomous cognitive filter that surfaces material corporate developments and generates primary-source research without financial hallucinations.

---

## 1. Product Vision & Core Architecture

FINN operates across two primary interaction workflows:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                               FINN ARCHITECTURE                                  │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│               PUSH WORKFLOW            │              PULL RAG WORKFLOW          │
│       (Proactive Portfolio Intel)      │     (Deep Primary-Grounded Research)    │
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ • 18 NSE Large-Cap Mock Portfolio      │ • Generalizes to ANY NSE Ticker         │
│ • Historical EOD (Oct 31, 2024) Prices │ • Faithful Annual Reports & Concalls    │
│ • 17-Category Filing Classifier        │ • PyMuPDF Page-by-Page Extraction       │
│ • Materiality Ranking (HIGH/MED/LOW)   │ • Audited Metric Provenance Ledger      │
│ • Daily Portfolio Briefings (24H/3D/7D)│ • Multi-Period Trajectory Tables & Trend│
│ • Configurable Price & Volume Triggers │ • Narrative vs Numbers & Bull vs Bear   │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

### A. Push — Proactive Portfolio Intelligence
* **Portfolio Watchlist**: 18 NSE-listed companies across 8 core sectors (`RELIANCE`, `TCS`, `INFY`, `WIPRO`, `HDFCBANK`, `ICICIBANK`, `SBIN`, `BAJFINANCE`, `JIOFIN`, `ONGC`, `TATAMOTORS`, `MARUTI`, `ITC`, `HINDUNILVR`, `SUNPHARMA`, `DRREDDY`, `BHARTIARTL`, `LT`).
* **Announcement Classification**: Classifies filings across all 17 reference categories from the ENAM Challenge Specification: `results`, `M&A`, `fund_raise`, `management_change`, `litigation`, `insider_trading`, `earnings_call`, `investor_meetings`, `credit_rating`, `dividend`, `bonus_split`, `capex`, `press_release`, `postal_ballot`, `agm_egm`, `pledging`, and `unclassified`.
* **Important Developments**: Automatically surfaces the top 3 highest priority developments with executive bio enrichment (for leadership changes) and headline financial cuts (for quarterly results).
* **Your Daily Portfolio Update**: Windowed digest (`24H`, `3D`, `7D`) answering: What happened? Which company? Why should an investor care? What is the source?
* **Configurable Alerts**: User-defined sliders for price moves ($\ge \pm3.0\%$) and volume spikes ($\ge 2.0\times$ 20-day MA) with one-click acknowledgement.

### B. Pull — Primary-Grounded Investment Research
* **Generalizes to ANY NSE Ticker**: Works for both portfolio stocks and ad-hoc tickers (e.g. `TCS`, `RELIANCE`, `HDFCBANK`, `TITAN`, `ZOMATO`).
* **Strict Primary Evidence**: Grounds insights exclusively in company-issued Annual Reports, Earnings Call Transcripts, and Result Disclosures. Secondary news articles and broker opinions are excluded.
* **Structured Research Report**:
  1. *Executive Summary*: High-conviction operational highlights and trajectory.
  2. *Business Overview*: Core industry verticals, geographical breakdown, order book TCV, and emerging technology pipelines.
  3. *Financial Snapshot*: Headline numbers + Audited Metric Provenance Ledger (Reported vs. Calculated, exact formulas, page citations).
  4. *Financial Performance Over Time*: Multi-period comparison table (`Q2 FY24`, `Q1 FY25`, `Q2 FY25`) with mathematically verified YoY% and QoQ% growth + visual trend charts.
  5. *Balance Sheet & Capital Structure*: Cash reserves, debt gearing (D/E), ROE, and explicit missing data disclosures.
  6. *Cash Flow Analysis*: Side-by-side reconciliation of PAT, Operating Cash Flow, and Free Cash Flow with cash conversion ratios and earnings quality evaluation.
  7. *Management Guidance vs. Actual Performance*: Direct contrast between past management promises and delivered operational execution.
  8. *Bull Case vs. Bear Case*: Distinct upside catalysts vs. downside risk factors.
  9. *Supporting Primary Documents*: Interactive citation cards opening an in-app primary filing inspector with verbatim extracted PDF text.
* **Anti-Hallucination Guardrail**: Queries for unindexed tickers (e.g. `TITAN`) display a clear warning with zero fabricated figures. Users can click `+ Upload filing PDF` to index any official 200+ page document into RAG immediately.

---

## 2. Technology Stack

* **Frontend**: Single-Page Application inspired by Linear and Notion dark mode (`#0A0F1A`), React 18, Tailwind CSS, Lucide icons, mobile-responsive layout (375px+ to 1440px+).
* **Backend**: Python 3.7+, FastAPI, Pydantic v2, Uvicorn.
* **PDF Ingestion**: PyMuPDF (`fitz`) for native page-by-page text and table extraction.
* **Vector Retriever**: Pure-Python TF-IDF and Cosine Similarity engine (zero C-library/DLL hurdles, 100% deterministic).
* **Storage**: Lightweight JSON / SQLite persistence.
* **PDF Extraction**: PyMuPDF (`fitz`) for page-by-page text and table extraction.
* **Retrieval Engine**: Pure-Python TF-IDF and Cosine Similarity vector retriever (zero DLL or external C-dependency hurdles, 100% deterministic and auditable).
* **AI Analysis**: Dual-mode engine:
  * *Production*: Gemini API / OpenAI API integration (via environment variables).
  * *Autonomous Institutional Fallback*: High-conviction deterministic extraction engine that operates with zero API key requirement, preventing application blocking.

---

## 3. Repository Structure

```
Enam Holdings/
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application & REST routing
│   ├── config.py                # Environment settings & threshold defaults
│   ├── models.py                # Pydantic schemas for portfolio, alerts, RAG
│   ├── stock_data.py            # 18-stock market data, volume ratios, P&L
│   ├── announcement_fetcher.py  # Regulatory announcement feed & ingestion
│   ├── announcement_classifier.py # 16-category hybrid classification
│   ├── priority_engine.py       # Heuristic materiality scoring & enrichment
│   ├── alert_engine.py          # Price/volume breach evaluation & settings
│   ├── digest_generator.py      # Windowed daily digest synthesis
│   ├── document_fetcher.py      # Primary PDF catalog & chunk indexing
│   ├── pdf_extractor.py         # PyMuPDF page-by-page extractor
│   ├── chunking.py              # Semantic financial chunker with page metadata
│   ├── retriever.py             # Pure-Python TF-IDF vector retrieval
│   ├── financial_analyzer.py    # Grounded 8-section research synthesis
│   ├── generate_seed_data.py    # Seed generator for 18 stocks & filings
│   └── generate_seed_docs.py    # Primary PDF filing & transcript generator
├── frontend/
│   ├── static/
│   │   └── index.html           # Full self-contained responsive terminal
│   ├── src/
│   │   ├── App.jsx              # Modular React App component
│   │   ├── api.js               # API client
│   │   ├── main.jsx             # React DOM root
│   │   └── index.css            # Custom terminal styling
│   ├── package.json             # Frontend dependency manifest
│   ├── vite.config.js           # Vite dev proxy configuration
│   └── tailwind.config.js       # Terminal dark-palette theme configuration
├── data/
│   ├── primary_documents/       # Real primary PDFs (TCS, RIL, HDFC Bank)
│   ├── portfolio_seed.json      # 18-company quotes, 30-day trends, holdings
│   └── announcements_seed.json  # Reference announcements across 16 categories
├── tests/
│   ├── __init__.py
│   ├── test_portfolio_data.py   # Portfolio valuation & volume tests
│   ├── test_classifier.py       # 16-category classification tests
│   ├── test_alerts.py           # Threshold breach & acknowledgement tests
│   ├── test_pdf_extraction.py   # PyMuPDF page extraction & chunking tests
│   └── test_retriever.py        # TF-IDF citation & narrative-vs-numbers tests
├── .env.example                 # Example configuration
├── .gitignore                   # Standard Python/Node ignore rules
├── requirements.txt             # Python dependencies
├── run_app.py                   # One-click unified application launcher
├── SUBMISSION_GUIDE.md          # Comprehensive evaluation & demo manual
└── README.md                    # Project documentation
```

---

## 4. Setup & Execution Instructions

### Prerequisites
* Python 3.7+ installed.

### Option A: One-Click Instant Launch (Recommended)
Clone the repository and run:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch FINN (Starts backend and serves mobile terminal on port 8000)
python run_app.py
```

Open your browser to:
* **Interactive Terminal**: [http://localhost:8000](http://localhost:8000)
* **Swagger API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Option B: Running via Vite Dev Server (Optional for Frontend Developers)
```bash
# Terminal 1: Backend
python -m backend.main

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

---

## 5. API Reference Summary

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/status` | `GET` | System health, primary doc index count, LLM status |
| `/api/portfolio` | `GET` | Complete 18-stock portfolio NAV, P&L, volume outliers |
| `/api/stocks/{ticker}` | `GET` | Stock quote & 30-day price trend for any ticker |
| `/api/announcements` | `GET` | Filter announcements by category, priority, or ticker |
| `/api/announcements` | `POST` | Ingest and auto-classify a new corporate filing |
| `/api/alerts` | `GET` | Active price move, volume spike, and filing alerts |
| `/api/alerts/acknowledge/{id}` | `POST` | Acknowledge/dismiss an active alert |
| `/api/alerts/settings` | `GET/POST` | Read or update price and volume thresholds |
| `/api/digest?window_hours=24` | `GET` | Windowed 4-part portfolio intelligence digest |
| `/api/research/query` | `POST` | On-demand primary-grounded Pull research |
| `/api/research/upload` | `POST` | Upload and index any genuine primary PDF into RAG corpus |
| `/api/research/documents/{ticker}` | `GET` | Catalog of primary documents indexed for a ticker |
| `/api/research/document/{id}/page/{n}` | `GET` | Inspect raw extracted text for a specific page citation |

---

## 6. Running the Test Suite

Run the full automated test suite (29 unit, integration, and data-integrity audit tests) covering portfolio math reconciliation, all 17 filing categories, alert triggers, PyMuPDF extraction, dynamic TF-IDF retrieval, PDF upload pipeline, and RAG quality enhancements:

```bash
python -m unittest discover -s tests
```

Expected output:
```
Ran 29 tests in 0.29s
OK
```

---

## 7. Financial Accuracy Rules & Data Integrity Disclosures

1. **Reconciled Portfolio Calculations**:
   * Total Portfolio Value: **₹81,93,516.00** (displayed as **₹81.94 lakh**).
   * Total Invested Capital: **₹75,26,800.00**.
   * Unrealized Gain/Loss: **₹6,66,716.00** (**+8.86%**).
   * Intraday P&L: **₹52,441.00** (**+0.64%**).
   * All figures across backend models, SQLite/JSON seed, API responses, automated tests, and the terminal dashboard are strictly derived from identical holdings and EOD market prices.
2. **Transparent Market Data Labeling**:
   * Market closing data is as of **October 31, 2024 (Historical EOD Close)**. It is explicitly labelled as historical closing data, never misrepresented as real-time live trading feeds.
3. **Primary Document Characterization**:
   * The baseline documents in `data/primary_documents/` (`TCS_Q2_FY25_Earnings_Call_Transcript.pdf`, `RELIANCE_Q2_FY25_Financial_Results_Notes.pdf`, `HDFCBANK_FY24_Annual_Report_Excerpts.pdf`) are **Curated Demonstration Excerpt Documents** compiled from authentic company disclosures, preserving authentic reported figures and page structures.
   * Full 200+ page official PDFs can be uploaded anytime via the UI or `POST /api/research/upload`, which immediately extracts and indexes all pages with PyMuPDF.
4. **Zero-Hallucination for Unindexed Tickers**:
   * If a user queries a ticker without an indexed primary document (e.g. `MARUTI` or `ZOMATO`), FINN returns an explicit warning (`"Primary document corpus missing on record"`) with zero hallucinated figures.
5. **Direct Page Verification**: Every finding references a specific document name and 1-based page number that can be inspected directly in the UI modal.

