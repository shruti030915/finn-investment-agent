from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class StockHistoryPoint(BaseModel):
    date: str
    close: float
    volume: int

class StockQuote(BaseModel):
    ticker: str
    name: str
    sector: str
    exchange: str = "NSE"
    symbol: str
    price: float
    prev_close: float
    change: float
    change_pct: float
    day_high: float
    day_low: float
    fifty_two_week_high: float
    fifty_two_week_low: float
    volume: int
    avg_volume_20d: int
    volume_multiple: float = 1.0
    market_cap_cr: float
    pe_ratio: float
    pb_ratio: float
    dividend_yield: float
    debt_to_equity: float
    roce: float
    roe: float
    shares_held: int = 0
    avg_buy_price: float = 0.0
    portfolio_weight: float = 0.0
    current_value: float = 0.0
    pnl: float = 0.0
    pnl_pct: float = 0.0
    history_30d: Optional[List[StockHistoryPoint]] = None

class PortfolioSummary(BaseModel):
    total_value_inr: float
    total_invested_inr: float
    total_pnl_inr: float
    total_pnl_pct: float
    day_change_inr: float
    day_change_pct: float
    stock_count: int
    top_gainers: List[StockQuote]
    top_losers: List[StockQuote]
    volume_outliers: List[StockQuote]
    stocks: List[StockQuote]

class AnnouncementEnrichment(BaseModel):
    type: str
    summary: Optional[str] = None
    executive_name: Optional[str] = None
    role: Optional[str] = None
    effective_date: Optional[str] = None
    background: Optional[str] = None
    target: Optional[str] = None
    deal_value: Optional[str] = None
    stake: Optional[str] = None
    strategic_rationale: Optional[str] = None
    analyst_implication: Optional[str] = None

class Announcement(BaseModel):
    id: str
    ticker: str
    company_name: str
    timestamp: str
    headline: str
    category: str
    priority: str  # HIGH, MEDIUM, LOW
    source: str
    source_doc_url: Optional[str] = None
    raw_text: str
    headline_numbers: Optional[Dict[str, Any]] = None
    enrichment: Optional[Dict[str, Any]] = None

class Alert(BaseModel):
    id: str
    ticker: str
    company_name: str
    timestamp: str
    alert_type: str  # PRICE_MOVE, UNUSUAL_VOLUME, MATERIAL_ANNOUNCEMENT
    priority: str    # HIGH, MEDIUM, LOW
    title: str
    description: str
    metric_value: Optional[float] = None
    threshold_value: Optional[float] = None
    details: Optional[Dict[str, Any]] = None
    acknowledged: bool = False

class AlertSettings(BaseModel):
    price_move_threshold: float = 3.0
    volume_mult_threshold: float = 2.0
    digest_window_hours: int = 24
    monitored_categories: List[str] = []

class DigestItem(BaseModel):
    ticker: str
    company_name: str
    priority: str
    category: str
    headline: str
    what_happened: str
    affected_entity: str
    why_investor_should_care: str
    source: str
    timestamp: str
    metrics: Optional[Dict[str, Any]] = None

class DailyDigest(BaseModel):
    generated_at: str
    window_hours: int
    total_filings_analyzed: int
    high_priority_count: int
    medium_priority_count: int
    executive_takeaway: str
    items: List[DigestItem]

class DocumentSourceItem(BaseModel):
    doc_id: str
    title: str
    ticker: str
    doc_type: str  # annual_report, earnings_transcript, results_filing, presentation
    page_number: int
    relevance_score: float
    snippet: str

class ResearchSection(BaseModel):
    title: str
    category: str
    content: str
    confidence: str  # REPORTED, CALCULATED, INTERPRETED
    key_metrics: Optional[Dict[str, Any]] = None
    sources: List[DocumentSourceItem] = []

class ResearchQueryRequest(BaseModel):
    ticker: str
    query: str = "Analyze financial trajectory, guidance vs actuals, and bull vs bear case"
    include_full_rag: bool = True

class ResearchResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    ticker: str
    company_name: str
    query: str
    analyzed_at: str
    model_used: str
    grounded_in_primary_sources: bool
    missing_data_disclosures: List[str] = []
    business_snapshot: ResearchSection
    financial_snapshot: ResearchSection
    financial_trajectory: ResearchSection
    balance_sheet_leverage: ResearchSection
    cash_quality_conversion: ResearchSection
    narrative_vs_numbers: ResearchSection
    bull_case: ResearchSection
    bear_case: ResearchSection
    all_cited_sources: List[DocumentSourceItem] = []
