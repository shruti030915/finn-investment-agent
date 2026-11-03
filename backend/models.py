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
    market_data_date: str = "2024-10-31"
    data_source: str = "EOD Verified Close (NSE)"
    is_live: bool = False
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
    original_filing_date: Optional[str] = None
    is_demo_data: bool = True
    data_origin: str = "DEMO DATA / SAMPLE FIXTURE"
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
    original_filing_date: Optional[str] = None
    is_demo_data: bool = True
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

class MetricProvenance(BaseModel):
    metric_name: str
    value: str
    unit: str
    period: str
    doc_id: str
    page_number: int
    figure_type: str  # "Reported" or "Calculated"
    formula: Optional[str] = None

class TrajectoryRow(BaseModel):
    metric: str
    q_prev_year: str
    q_prev: str
    q_current: str
    yoy_growth: str
    qoq_growth: str

class TrendChartPoint(BaseModel):
    period: str
    revenue_cr: Optional[float] = None
    ebit_cr: Optional[float] = None
    pat_cr: Optional[float] = None
    fcf_cr: Optional[float] = None

class CashQualityComparison(BaseModel):
    pat_value: str
    ocf_value: str
    fcf_value: str
    conversion_ratio: str
    conversion_quality: str
    pat_provenance: str
    ocf_provenance: str
    fcf_provenance: str
    assessment: str

class ResearchSection(BaseModel):
    title: str
    category: str
    content: str
    confidence: str  # REPORTED, CALCULATED, INTERPRETED, UNAVAILABLE
    key_metrics: Optional[Dict[str, Any]] = None
    detailed_metrics: List[MetricProvenance] = []
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
    trajectory_table: List[TrajectoryRow] = []
    trajectory_chart: List[TrendChartPoint] = []
    cash_comparison: Optional[CashQualityComparison] = None
    all_metrics_provenance: List[MetricProvenance] = []
