import os
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, Body, Request
import shutil
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import (
    HOST, PORT, DEBUG, FRONTEND_DIST_DIR, STATIC_DIR,
    DEFAULT_MONITORED_CATEGORIES, ALL_CATEGORIES, GEMINI_API_KEY, OPENAI_API_KEY
)
from backend.models import (
    PortfolioSummary, StockQuote, Announcement, Alert, AlertSettings,
    DailyDigest, ResearchQueryRequest, ResearchResponse
)
from backend.stock_data import stock_manager
from backend.announcement_fetcher import announcement_manager
from backend.alert_engine import alert_engine
from backend.digest_generator import digest_generator
from backend.financial_analyzer import financial_analyzer
from backend.document_fetcher import document_fetcher

logging.basicConfig(level=logging.INFO if not DEBUG else logging.DEBUG)
logger = logging.getLogger("finn.api")

app = FastAPI(
    title="FINN — Financial Investment Intelligence Agent",
    description="Proactive Push & Deep Pull Financial Research Agent for ENAM Holdings",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SYSTEM & STATUS ---

@app.get("/api/status")
def get_system_status():
    return {
        "status": "online",
        "app": "FINN — Financial Investment Intelligence Agent",
        "portfolio_stock_count": len(stock_manager.get_all_portfolio_stocks()),
        "indexed_documents_count": len(document_fetcher._documents),
        "indexed_chunks_count": len(document_fetcher.get_all_chunks()),
        "llm_provider": "Gemini" if GEMINI_API_KEY else ("OpenAI" if OPENAI_API_KEY else "FINN Institutional Deterministic RAG (Offline & Autonomous)"),
        "active_alerts_count": len([a for a in alert_engine.evaluate_alerts() if not a.acknowledged])
    }

# --- PUSH: PORTFOLIO & MARKET DATA ---

@app.get("/api/portfolio", response_model=PortfolioSummary)
def get_portfolio():
    return stock_manager.get_portfolio_summary()

@app.get("/api/stocks/{ticker}", response_model=StockQuote)
def get_stock_detail(ticker: str):
    stock = stock_manager.get_stock(ticker)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock ticker {ticker} not found")
    return stock

# --- PUSH: CORPORATE ANNOUNCEMENTS ---

@app.get("/api/announcements", response_model=List[Announcement])
def get_announcements(
    ticker: Optional[str] = Query(None, description="Filter by NSE ticker"),
    priority: Optional[str] = Query("ALL", description="Filter by priority: HIGH, MEDIUM, LOW, or ALL"),
    category: Optional[str] = Query("all", description="Filter by category or 'all'"),
    window_hours: Optional[int] = Query(None, description="Time window in hours")
):
    return announcement_manager.get_announcements(
        ticker=ticker,
        priority=priority,
        category=category,
        window_hours=window_hours
    )

@app.post("/api/announcements", response_model=Announcement)
def ingest_announcement(data: dict = Body(...)):
    if "headline" not in data or "ticker" not in data:
        raise HTTPException(status_code=400, detail="Missing headline or ticker in announcement submission")
    return announcement_manager.add_announcement(data)

# --- PUSH: ALERTS & CONFIGURATION ---

@app.get("/api/alerts", response_model=List[Alert])
def get_active_alerts():
    return alert_engine.evaluate_alerts()

@app.post("/api/alerts/acknowledge/{alert_id}")
def acknowledge_alert(alert_id: str):
    return alert_engine.acknowledge_alert(alert_id)

@app.get("/api/alerts/settings", response_model=AlertSettings)
def get_alert_settings():
    return alert_engine.get_settings()

@app.post("/api/alerts/settings", response_model=AlertSettings)
def update_alert_settings(settings: AlertSettings):
    alert_engine.update_settings(settings)
    return alert_engine.get_settings()

@app.get("/api/categories")
def get_available_categories():
    return {"all_categories": ALL_CATEGORIES, "default_monitored": DEFAULT_MONITORED_CATEGORIES}

# --- PUSH: DAILY DIGEST ---

@app.get("/api/digest", response_model=DailyDigest)
def get_daily_digest(window_hours: int = Query(24, ge=1, le=168)):
    return digest_generator.generate_digest(window_hours=window_hours)

# --- PULL: ON-DEMAND RESEARCH & RAG ---

@app.post("/api/research/query", response_model=ResearchResponse)
def run_company_research(request: ResearchQueryRequest):
    if not request.ticker:
        raise HTTPException(status_code=400, detail="Stock ticker is required for research")
    return financial_analyzer.analyze_company(request)

@app.post("/api/research/upload")
async def upload_primary_document(request: Request, filename: Optional[str] = Query(None), ticker: Optional[str] = Query(None)):
    pdf_bytes = await request.body()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty request body. Please provide PDF file bytes.")
    
    result = document_fetcher.save_and_index_pdf(filename=filename, pdf_bytes=pdf_bytes, ticker=ticker)
    return result

@app.get("/api/research/documents/{ticker}")
def get_documents_for_ticker(ticker: str):
    docs = document_fetcher.get_documents_for_ticker(ticker)
    return [
        {
            "doc_id": d["doc_id"],
            "title": d["title"],
            "doc_type": d["doc_type"],
            "ticker": d["ticker"],
            "page_count": d["page_count"]
        }
        for d in docs
    ]

@app.get("/api/research/document/{doc_id}/page/{page_number}")
def get_document_page_text(doc_id: str, page_number: int):
    page = document_fetcher.get_document_page(doc_id, page_number)
    if not page:
        raise HTTPException(status_code=404, detail=f"Page {page_number} in document {doc_id} not found")
    return page

# --- STATIC & FRONTEND SPA SERVING ---

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "app": "FINN — Financial Investment Intelligence Agent",
        "api_docs": "/docs",
        "status": "/api/status"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=DEBUG)

