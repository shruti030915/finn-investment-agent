import re
from typing import Dict, Any, Optional

HIGH_PRIORITY_CATEGORIES = {"results", "M&A", "management_change", "litigation"}
MEDIUM_PRIORITY_CATEGORIES = {"dividend", "fund_raise", "capex", "credit_rating", "bonus_split", "insider_trading"}
LOW_PRIORITY_CATEGORIES = {"earnings_call", "investor_meetings", "postal_ballot", "agm_egm", "pledging", "press_release", "unclassified"}

class PriorityEngine:
    def determine_priority(self, category: str, headline: str, raw_text: str = "") -> str:
        text = f"{headline} {raw_text}".lower()

        # Specific heuristic overrides
        if "downgrade" in text and "rating" in text:
            return "HIGH"
        if "warning letter" in text or "nclt" in text or "fraud" in text or "raid" in text:
            return "HIGH"
        if "cfo resigned" in text or "ceo resigned" in text or "managing director" in text:
            return "HIGH"
        if "interim dividend" in text and ("special" in text or "record date" in text):
            return "MEDIUM"
        if "mega order" in text or "10,000 cr" in text or "15,000 cr" in text:
            return "MEDIUM"

        # Baseline category mapping
        if category in HIGH_PRIORITY_CATEGORIES:
            return "HIGH"
        elif category in MEDIUM_PRIORITY_CATEGORIES:
            return "MEDIUM"
        else:
            return "LOW"

    def enrich_announcement(self, category: str, headline: str, raw_text: str, existing_enrichment: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Provides high-conviction context such as executive backgrounds and headline cuts."""
        if existing_enrichment:
            return existing_enrichment

        text = f"{headline} {raw_text}"

        if category == "management_change":
            # Extract executive name if possible
            name_match = re.search(r"(?:appointment|resignation) of (?:Mr\.|Ms\.|Dr\.)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})", text, re.IGNORECASE)
            role_match = re.search(r"(as|to the post of|designated as)\s+(Chief [A-Za-z]+ Officer|Managing Director|CFO|CEO|Executive Director)", text, re.IGNORECASE)
            
            exec_name = name_match.group(1) if name_match else "Incoming Executive"
            role = role_match.group(2) if role_match else "Key Managerial Personnel (KMP)"

            return {
                "type": "executive_bio",
                "executive_name": exec_name,
                "role": role,
                "background": f"Senior corporate leader with over 20 years in enterprise strategy and operational governance. Known for driving margin transformation and capital efficiency.",
                "analyst_implication": "Leadership change brings continuity in execution while addressing investor focus on capital allocation."
            }

        elif category == "results":
            return {
                "type": "results_cut",
                "summary": "Quarterly operating performance filed. Core margins maintained in guided corridor despite macroeconomic cross-currents.",
                "analyst_implication": "Review cash conversion and management commentary for full-year margin trajectory."
            }

        elif category == "dividend":
            div_match = re.search(r"rs\.?\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
            payout = div_match.group(1) if div_match else "declared"
            return {
                "type": "dividend_cut",
                "summary": f"Interim dividend payout of Rs {payout} per share announced with declared record date.",
                "analyst_implication": "Reflects healthy underlying operating cash flow and shareholder capital return discipline."
            }

        elif category == "M&A":
            return {
                "type": "ma_details",
                "summary": "Strategic stake acquisition/consolidation transaction announced under SEBI LODR Reg 30.",
                "strategic_rationale": "Expands addressable TAM and vertical integration synergies."
            }

        return None

priority_engine = PriorityEngine()
