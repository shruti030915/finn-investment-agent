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

1. **Portfolio Overview**:
   * Open the **HOME** tab.
   * Review the 18 NSE-listed companies across 8 sectors in the top real-time ticker tape and portfolio summary cards.
   * Notice real-time NAV calculations, intraday gain/loss, and volume outlier tracking.

2. **Windowed Daily Digest**:
   * Inspect the **Windowed Portfolio Intelligence Digest** card.
   * Toggle between **24H**, **3D**, and **7D** time windows.
   * Observe the four core answers synthesized for each major event:
     * *What happened?*
     * *Which company is affected?*
     * *Why should an investor care?*
     * *What is the verifiable source?*

3. **High-Value Announcement Enrichment**:
   * Scroll down to the **Filtered Corporate Announcement Stream**.
   * Locate the **WIPRO** management change: notice the extracted executive background bio (previous roles, education, track record).
   * Locate the **TCS** quarterly results filing: notice the headline cuts (Revenue, EBITDA margin, PAT) with QoQ and YoY comparisons.
   * Filter the stream by category (`results`, `M&A`, `dividend`, `litigation`, etc.) or priority (`HIGH`, `MEDIUM`, `LOW`).

4. **Configurable Triggered Alerts**:
   * Click on the **ALERTS** tab.
   * Observe active alerts triggered by:
     * **Price movement breach** (e.g., WIPRO $+4.22\%$, BAJFINANCE $-3.53\%$).
     * **Unusual volume spike** (e.g., WIPRO $2.45\times$, SUNPHARMA $2.33\times$ 20-day MA).
     * **Material announcements** (M&A, litigation, leadership changes).
   * Adjust the **Price Movement Threshold** slider (e.g., set to $\pm4.0\%$) and click **Apply Thresholds**; observe the alerts dynamically updating.
   * Click **Dismiss** on an alert to test acknowledgement.

---

## 3. Demonstrating the Pull Research Workflow

1. **Select or Enter Any NSE Ticker**:
   * Switch to the **PULL RAG** tab.
   * Click the **TCS** chip (or type any other ticker, such as `RELIANCE`, `HDFCBANK`, `TITAN`, or `ZOMATO`).
   * Select a research query preset or enter a custom prompt (e.g., *"Compare management guidance with actual performance"*).
   * Click **Run Analysis**.

2. **Inspect the 8-Section Institutional Report**:
   * **Business Snapshot**: Core business verticals, segment mix, and geographical exposure.
   * **Financial Snapshot**: Current headline metrics, distinguishing Reported from Calculated metrics.
   * **Financial Trajectory**: Multi-year direction, what is expanding, and what is compressing.
   * **Balance Sheet & Leverage**: Funding structure, debt gearing (D/E), and working capital metrics.
   * **Cash Quality**: Free cash flow generation and cash conversion efficiency (OCF vs. PAT).
   * **Narrative vs. Numbers (Critical Evaluation)**: Compares what management promised over the last four quarters against delivered operational execution (e.g., North American BFSI discretionary spend slowdown).
   * **Institutional Bull & Bear Theses**: High-conviction cases for both upside catalysts and downside risks.

3. **Verify Auditable Primary Document Citations**:
   * Scroll to the **Supporting Primary Documents** section at the bottom of the research view.
   * Click on any citation item (e.g., `TCS_Q2_FY25_Earnings_Call_Transcript.pdf — Page 2`).
   * An in-app **Primary Filing Inspector** modal will open, displaying the exact text and tables extracted from the physical PDF using PyMuPDF.

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

