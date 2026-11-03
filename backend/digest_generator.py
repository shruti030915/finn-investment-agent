from datetime import datetime
from typing import List
from backend.models import DailyDigest, DigestItem
from backend.announcement_fetcher import announcement_manager

class DigestGenerator:
    def generate_digest(self, window_hours: int = 24) -> DailyDigest:
        announcements = announcement_manager.get_announcements(window_hours=window_hours)
        # Prioritize HIGH and MEDIUM
        high_prio = [a for a in announcements if a.priority == "HIGH"]
        med_prio = [a for a in announcements if a.priority == "MEDIUM"]
        low_prio = [a for a in announcements if a.priority == "LOW"]

        digest_items: List[DigestItem] = []

        for ann in high_prio + med_prio:
            # Determine Why Investor Should Care
            why_care = "Operational update with potential implications on forward business trajectory."
            if ann.category == "results":
                rev_growth = ann.headline_numbers.get("revenue_yoy_pct", "healthy") if ann.headline_numbers else "solid"
                margin = ann.headline_numbers.get("ebitda_margin_pct", "stable") if ann.headline_numbers else "healthy"
                why_care = f"Directly reflects core operating resilience: Revenue YoY {rev_growth}%, Operating Margin {margin}%. Determines earnings revision cycle."
            elif ann.category == "management_change":
                role = ann.enrichment.get("role", "Leadership") if ann.enrichment else "Key Leadership"
                why_care = f"{role} transition introduces strategic continuity test and organizational capital allocation priorities."
            elif ann.category == "litigation":
                why_care = "Regulatory action introduces potential compliance remediation overhead and regulatory scrutiny; monitors impact on overseas filings."
            elif ann.category == "M&A":
                why_care = "Capital deployment into strategic expansion; validates inorganic growth initiatives and synergistic revenue upside."
            elif ann.category == "dividend":
                why_care = "Direct cash return to shareholders; signals balance sheet strength, free cash flow generation, and management payout discipline."
            elif ann.category == "capex":
                why_care = "Expansion of multi-year contract backlog; elevates long-term revenue visibility and fixed asset utilization."
            elif ann.category == "credit_rating":
                why_care = "Reaffirmation/upgrade protects institutional borrowing cost spreads and safeguards debt capital market access."
            elif ann.category == "insider_trading":
                why_care = "Promoter stake increase signals high alignment with minority shareholders and internal conviction at current market valuations."

            digest_items.append(DigestItem(
                ticker=ann.ticker,
                company_name=ann.company_name,
                priority=ann.priority,
                category=ann.category,
                headline=ann.headline,
                what_happened=ann.raw_text,
                affected_entity=f"{ann.company_name} ({ann.ticker}.NS)",
                why_investor_should_care=why_care,
                source=f"{ann.source} [DEMO FIXTURE]",
                timestamp=ann.timestamp,
                original_filing_date=ann.original_filing_date,
                is_demo_data=ann.is_demo_data,
                metrics=ann.headline_numbers
            ))

        # Executive takeaway
        if high_prio:
            lead_tickers = ", ".join(list(dict.fromkeys([a.ticker for a in high_prio])))
            exec_summary = (
                f"During the last {window_hours} hours, {len(announcements)} exchange disclosures were monitored. "
                f"Actionable material developments surfaced in {lead_tickers}, led by Q2 earnings filings, leadership realignment, "
                f"and strategic corporate actions. Routine regulatory compliance filings ({len(low_prio)} items) have been safely collapsed."
            )
        else:
            exec_summary = (
                f"No critical risk breaches across monitored portfolio during the last {window_hours} hours. "
                f"{len(announcements)} disclosures reviewed, all classified within standard operational parameters."
            )

        return DailyDigest(
            generated_at=datetime.now().isoformat(),
            window_hours=window_hours,
            total_filings_analyzed=len(announcements),
            high_priority_count=len(high_prio),
            medium_priority_count=len(med_prio),
            executive_takeaway=exec_summary,
            items=digest_items
        )

digest_generator = DigestGenerator()

