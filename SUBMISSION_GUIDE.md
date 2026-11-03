# FINN — Submission & Evaluation Manual
### ENAM Holdings AI Engineer Build Challenge

---

## 1. Quick Launch Instructions

To launch the complete application (both the backend REST API and the mobile-first frontend):

```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Run one-click launcher
python run_app.py
```

Open your browser to:
* **Interactive Terminal**: [http://localhost:8000](http://localhost:8000)
* **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

*(Tip: In Chrome or Safari, press `F12` or `Ctrl+Shift+M` / `Cmd+Shift+M` to inspect the UI in mobile device view, such as iPhone 14 Pro or Pixel 7).*

---

## 2. Demonstrating the Push Workflow

1. **Portfolio Overview & Watchlist**:
   * Open the **Home** tab.
   * View the 4 key portfolio metrics: Portfolio Value (**₹81.94 lakh** / `₹81,93,516`), Today's Gain (**+₹52,441** / `+0.64%`), Total Unrealized Gain (**+₹6,66,716**), and Overall Return (**+8.86%**).
   * Note the transparent label: `Market close: Oct 31, 2024 • Curated Disclosures`.
   * Review the compact **Portfolio Watchlist** table showing prices, changes, and 20-day volume multiples for all 18 holdings across 8 sectors.

2. **Important Developments**:
   * Inspect the **Important developments** card at the top of the Home view.
   * Highlights the top 3 critical events requiring investor attention (e.g. TCS Q2 FY25 results, WIPRO leadership change, BAJFINANCE volume breach) with explicit "Why it matters" rationales and quick links to research.

3. **Your Daily Portfolio Update**:
   * Toggle between **24H**, **3D**, and **7D** filters.
   * Review the high-level **Executive Takeaway** and browse disclosures.
   * Click **Read more details** on any disclosure to expand the complete context without leaving the dashboard.

4. **Alerts & Threshold Controls**:
   * Click on the **Alerts** tab.
   * View active price breach alerts (Wipro $+4.22\%$, Bajaj Finance $-3.53\%$) and volume spike alerts (Wipro $2.45\times$, Sun Pharma $2.33\times$).
   * Adjust the **Price Move Trigger** and **Volume Spike Trigger** sliders and click **Save Thresholds**.
   * Click **Dismiss** on an active alert to test acknowledgement.

---

## 3. Demonstrating the Pull Research Workflow

1. **Enter Any NSE Ticker**:
   * Switch to the **Research** tab.
   * Click the **TCS** chip (or type any other ticker, such as `RELIANCE`, `HDFCBANK`, `INFY`, or unindexed tickers like `TITAN` and `ZOMATO`).
   * Select a preset prompt or type a custom question.
   * Click **Analyse company**.

2. **Inspect the 9-Section Institutional Report**:
   * **Executive Summary**: High-conviction operational highlights and trajectory.
   * **Business Overview**: Segment mix (Energy +7.0%, Manufacturing +5.3%, BFSI 31.3%), geographical performance (UK +4.6%, North America -2.1%), deal TCV ($8.6B), and GenAI pipeline ($1.5B).
   * **Financial Snapshot**: Headline metrics + **Audited Metric Provenance & Calculation Ledger** (Reported vs. Calculated, exact formulas, and page numbers).
   * **Financial Performance Over Time**: Multi-period comparison table (`Q2 FY24`, `Q1 FY25`, `Q2 FY25`) with verified YoY% and QoQ% growth + visual trend charts.
   * **Balance Sheet & Capital Structure**: Zero debt gearing (D/E 0.00), liquid reserves (₹43,892 Cr), ROE (51.2%), and explicit missing disclosure notice for total assets.
   * **Cash Flow Analysis**: Side-by-side reconciliation of PAT (₹11,909 Cr), Operating Cash Flow (₹11,261 Cr), and Free Cash Flow (₹11,261 Cr) with verified calculated conversion ratio (94.56%), management standalone explanation (100.2%), and capex note.
   * **Management Guidance vs. Actual Performance**: Direct contrast between past management promises and delivered operational execution.
   * **Bull Case vs. Bear Case**: 4 distinct bull catalysts and 4 distinct bear headwinds.
   * **Supporting Primary Documents**: Click any citation card to open the in-app **Primary Filing Inspector modal** with verbatim extracted PDF text.

3. **Verify Anti-Hallucination & PDF Upload**:
   * Type **`TITAN`** or **`ZOMATO`** into the ticker search and click **Analyse company**.
   * Observe the clear amber notice: *"Primary document not yet indexed for TITAN. Analysis is restricted to verifiable market data."* Notice zero fabricated quotes or fake figures.
   * Click **+ Upload filing PDF** to upload any official company PDF and observe immediate PyMuPDF extraction and vector indexing.

---

## 4. Suggested Screenshots to Capture for Submission

1. **Desktop / Mobile Home View**: Showing the portfolio ticker tape, portfolio NAV metrics, critical attention banners, and windowed daily digest.
2. **Alerts Terminal**: Displaying triggered unusual volume anomalies, price volatility alerts, and the configurable threshold slider controls.
3. **Pull Research (Narrative vs. Numbers)**: Highlighting the contrast between management forward guidance and actual financial delivery.
4. **Primary Source Citation Inspector**: Showing the modal with exact page citations and extracted primary PDF text.
5. **Mobile Viewport**: Demonstrating the bottom navigation bar and mobile-first responsive layout on a smartphone screen.

---

## 5. Deployment Guide (Free Tier Ready)

FINN is engineered to deploy seamlessly to any cloud host:

### Deploy to Render / Railway / DigitalOcean
1. Push your repository to GitHub.
2. Connect your repository on Render or Railway as a **Web Service**.
3. Set:
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `python run_app.py`
   * **Environment Variables**: Set `FINN_PORT=8000` (or host-assigned port), and optionally `GEMINI_API_KEY`.
4. Deploy. The web application will immediately serve the responsive mobile terminal.

---

## 6. Covering Email Draft

Copy, personalize, and send to: **assessment@enam.com**  
**Subject**: `ENAM - IIT screening - 2027`

```text
To: assessment@enam.com
Subject: ENAM - IIT screening - 2027

Dear ENAM Holdings Investment & Engineering Team,

Please find my submission for the ENAM Holdings AI Engineer Build Challenge below.

1. DELIVERABLES & LINKS
--------------------------------------------------
• GitHub Repository: https://github.com/[YOUR-USERNAME]/finn-investment-agent
• Live Deployed Prototype: https://[YOUR-DEPLOYED-URL].onrender.com (or local demo video/screenshots attached)
• AI Build History & Prompts: [Link to Cursor / Claude Code / Antigravity transcript export]

2. WHAT I BUILT: FINN (FINANCIAL INVESTMENT AGENT)
--------------------------------------------------
FINN is a mobile-first financial intelligence layer engineered for public-market investors that operates in two primary modes:

A. PUSH — Proactive Market Intelligence:
• Monitors a mock portfolio of 18 NSE large-cap companies across 8 core sectors with reconciled portfolio math (NAV: ₹81,93,516.00 / ₹81.94L, Invested: ₹75,26,800.00, P&L: ₹6,66,716.00 / +8.86%, Day's Gain: ₹52,441.00 / +0.64%).
• Tracks historical EOD closing prices (as of October 31, 2024) and volume multiples against 20-day historical moving averages.
• Hybrid classification across all 17 corporate announcement categories from the reference brief.
• Heuristic materiality ranking (HIGH, MEDIUM, LOW) that prioritizes results, M&A, leadership changes, and litigation, while filtering routine compliance paperwork.
• Enriched presentation: extracts incoming executive bios for management changes and headline quarterly cuts (Revenue, EBITDA margin, PAT) with QoQ and YoY comparisons.
• Windowed daily portfolio digest (24h/3d/7d) answering: What happened? Which company? Why should an investor care? What is the source?
• User-configurable price movement (±%) and unusual volume multiplier thresholds.

B. PULL — Primary-Grounded Company Research:
• Researches ANY NSE ticker (works for both portfolio stocks and ad-hoc tickers like TCS, RELIANCE, HDFCBANK, TITAN, ZOMATO).
• Grounded strictly in primary company documents: initial curated demonstration excerpts for TCS, Reliance, and HDFC Bank, plus a working in-browser/API PDF upload engine (`POST /api/research/upload`) to index any authentic 200+ page company Annual Report.
• Pure-Python TF-IDF vector retrieval over chunked pages with exact document and 1-based page citations.
• Synthesizes an 8-part institutional research report: Business Snapshot, Financial Snapshot, Trajectory, Balance Sheet, Cash Quality, Narrative vs. Numbers (promised guidance vs. actual execution), and Bull vs. Bear cases.
• Complies with financial accuracy rules: returns explicit warning for unindexed tickers without hallucinating figures, differentiates reported vs. calculated vs. interpreted figures, and includes an in-app primary filing inspector modal.
• Verified with 21 automated unit, integration, and data-integrity audit tests.

3. KEY ARCHITECTURAL DECISIONS & TRADE-OFFS
--------------------------------------------------
• Zero-Failure Dual-Mode Execution: Designed with both a production LLM integration and an autonomous institutional deterministic RAG engine. If an API key is missing or an external service rate-limits, FINN continues operating reliably without blocking the user.
• Resilient Retrieval: Engineered a pure-Python TF-IDF cosine similarity engine to eliminate external C-library / DLL permission hurdles on Windows and cloud environments.
• High Information Density: Modeled the UI after the Bloomberg Terminal's compact typography and modern fintech design (deep navy palette, emerald positive, crimson alert indicators).

4. WHAT I DELIBERATELY LEFT OUT
--------------------------------------------------
• Complex multi-agent orchestration frameworks (e.g. CrewAI/AutoGen), which add latency and non-deterministic execution failure points for a time-constrained investor workflow.
• Live scraping of volatile exchange endpoints, substituting a robust ingestion API and verified primary filing seed corpus.

5. WHERE I WOULD TAKE IT NEXT
--------------------------------------------------
• Real-time webhook ingestion for BSE/NSE XBRL disclosures.
• Automated tabular reconciliation comparing concall guidance numbers directly against subsequent XBRL balance sheet filings.
• WhatsApp / Telegram daily windowed executive digest delivery.

Thank you for the opportunity to participate in this challenge. I welcome the opportunity to discuss the architecture and product design further.

Best regards,
[Your Name]
[Your Contact Information / IIT Roll Number]
```

