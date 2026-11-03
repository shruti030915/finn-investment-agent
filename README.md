# FINN — Financial Investment Intelligence Agent
### Developed for the ENAM Holdings AI Engineer Build Challenge

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.22+-orange.svg)](https://pymupdf.readthedocs.io/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Dark%20Terminal-0F172A.svg)](https://tailwindcss.com)
[![Architecture](https://img.shields.io/badge/Architecture-Push%20%2B%20Pull%20RAG-indigo.svg)]()

FINN is a mobile-first financial intelligence layer engineered for high-conviction public-market investors at ENAM Holdings. Public market investors are inundated with daily market noise—filings, press releases, price movements, and macro commentary. FINN operates as an autonomous cognitive filter that surfaces only what matters and buries routine compliance disclosures.

---

## 1. Product Vision & Two Interaction Modes

FINN operates in two complementary interaction modalities:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                               FINN ARCHITECTURE                                  │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│               PUSH MODE                │                PULL MODE                │
│    (Proactive Market Intelligence)     │      (Deep Primary-Grounded RAG)        │
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ • 18 NSE Large-Cap Mock Portfolio      │ • Generalizes to ANY NSE Ticker         │
│ • EOD Price & Volume Tracking          │ • Audited Annual Reports & Concalls     │
│ • 16-Category Filing Classifier        │ • PyMuPDF Page-by-Page Extraction       │
│ • Heuristic Materiality Priority Engine│ • Strict Document & Page Citations      │
│ • Windowed Daily Digest (24H / 3D / 7D)│ • Narrative vs. Numbers Evaluation      │
│ • Configurable Price & Volume Triggers │ • Institutional Bull vs. Bear Theses    │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

### A. Push — Proactive Financial Intelligence
* **Mock Portfolio**: 18 NSE-listed companies across 8 core sectors (`RELIANCE`, `TCS`, `INFY`, `WIPRO`, `HDFCBANK`, `ICICIBANK`, `SBIN`, `BAJFINANCE`, `JIOFIN`, `ONGC`, `TATAMOTORS`, `MARUTI`, `ITC`, `HINDUNILVR`, `SUNPHARMA`, `DRREDDY`, `BHARTIARTL`, `LT`).
* **Announcement Classification**: Classifies filings across all 17 reference categories from the ENAM Challenge Specification: `results`, `M&A`, `fund_raise`, `management_change`, `litigation`, `insider_trading`, `earnings_call`, `investor_meetings`, `credit_rating`, `dividend`, `bonus_split`, `capex`, `press_release`, `postal_ballot`, `agm_egm`, `pledging`, and `unclassified`.
* **Priority Engine**:
  * **HIGH**: Quarterly/Annual results, M&A/demergers, leadership shifts (CEO/CFO), critical litigation (FDA warnings).
  * **MEDIUM**: Interim dividends, capital expenditure, debt ratings, insider buying.
  * **LOW**: Routine compliance certificates (e.g. Reg 74(5), duplicate share certificates, postal ballot procedural notices).
* **High-Conviction Presentation**:
  * *Management changes* are automatically enriched with executive biographies (background, former company, qualifications).
  * *Quarterly results* filings extract headline cuts (Revenue, EBITDA margin, PBT, PAT) with QoQ and YoY variances.
* **Windowed Portfolio Digest**: Concise briefings addressing four specific questions:
  1. *What happened?*
  2. *Which company is affected?*
  3. *Why should an investor care?*
  4. *What is the verifiable source?*
* **Configurable Alerts**: User-defined thresholds for daily price moves (e.g., $\ge \pm3.0\%$), unusual volume spikes (e.g., $\ge 2.0\times$ 20-day moving average), and category filters.

### B. Pull — Primary-Grounded Company Research
* **Generalizes to ANY NSE Ticker**: Researches both portfolio holdings and ad-hoc tickers (e.g., `TCS`, `RELIANCE`, `HDFCBANK`, `TITAN`, `ZOMATO`, `ASIANPAINT`).
* **Strict Primary Evidence**: Grounds insights exclusively in audited Annual Reports, Earnings Call (concall) Transcripts, and Financial Result Disclosures. Secondary sources, news commentary, and broker notes are explicitly excluded.
* **8-Section Institutional Report**:
  1. *Business Snapshot*: Core segments, business model, and revenue mix.
  2. *Financial Snapshot*: Headline numbers (Reported vs. Calculated vs. Interpreted).
  3. *Financial Trajectory*: Multi-year operational direction and margin expansion/compression.
  4. *Balance Sheet & Leverage*: Funding structure, debt gearing (D/E), and working-capital cycles.
  5. *Cash Quality*: Cash conversion efficiency (Operating Cash Flow vs. Net Profit, FCF).
  6. *Narrative vs. Numbers*: Evaluates what management promised over the last four quarters against delivered operational execution.
  7. *Bull Case*: High-conviction investment thesis.
  8. *Bear Case*: Critical downside risks, operational vulnerabilities, and valuation headwinds.
* **Auditable Citations**: Every finding cites the exact document title and 1-based page number, complete with an interactive primary source inspector modal.

---

## 2. Technology Stack

* **Frontend**: Responsive Single-Page Application with dark Bloomberg-terminal aesthetics (`#080C14`), React 18, Tailwind CSS, Lucide icons, and high-density responsive layout (optimized for mobile 375px+ and desktop 1440px+).
* **Backend**: Python, FastAPI, Pydantic v2, Uvicorn.
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

Run the full automated test suite (21 unit and data-integrity audit tests) covering portfolio math reconciliation, all 17 filing categories, alert triggers, PyMuPDF extraction, dynamic TF-IDF retrieval, and the PDF upload pipeline:

```bash
python -m unittest discover -s tests
```

Expected output:
```
Ran 21 tests in 0.17s
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

