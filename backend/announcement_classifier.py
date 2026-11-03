import re
from typing import Tuple

KEYWORD_CATEGORY_RULES = [
    # results
    (r"\b(financial results|unaudited results|audited results|board meeting.*results|q[1-4]\s*(fy\d{2})?|results press release|quarterly results|annual results)\b", "results"),
    # M&A
    (r"\b(merger|acquisition|amalgamation|demerger|joint venture|scheme of arrangement|strategic investment|stake sale|acqui\w+)\b", "M&A"),
    # fund_raise
    (r"\b(fund\s*raise|rights issue|qip|preferential allotment|buyback|commercial paper|ncd|non-convertible debentures|issuance of equity)\b", "fund_raise"),
    # management_change
    (r"\b(appointment of|resignation of|cessation of|chief executive officer|chief financial officer|managing director|kmp|key managerial personnel|ceo|cfo|md\b|executive director)\b", "management_change"),
    # litigation
    (r"\b(warning letter|fda 483|show cause notice|litigation|lawsuit|arbitration|penalty|fine imposed|sebi order|nclt|insolvency|regulatory action)\b", "litigation"),
    # insider_trading
    (r"\b(pit regulations|insider trading|promoter acquisition|promoter disposal|regulation 7\(2\)|insider buying)\b", "insider_trading"),
    # earnings_call
    (r"\b(earnings call|concall|conference call.*results|audio recording.*call|transcript.*call)\b", "earnings_call"),
    # investor_meetings
    (r"\b(investor meet|analyst meet|institutional investor|investor conference|schedule of analyst)\b", "investor_meetings"),
    # credit_rating
    (r"\b(credit rating|crisil|icra|care ratings|india ratings|rating reaffirmed|rating upgraded|rating downgraded)\b", "credit_rating"),
    # dividend
    (r"\b(dividend|interim dividend|final dividend|special dividend|record date.*dividend)\b", "dividend"),
    # bonus_split
    (r"\b(bonus issue|bonus shares|sub-division of shares|stock split|face value split)\b", "bonus_split"),
    # capex
    (r"\b(capex|capital expenditure|new plant|capacity expansion|commissioning of|order win|mega order|contract win)\b", "capex"),
    # postal_ballot
    (r"\b(postal ballot|scrutinizer report.*postal ballot)\b", "postal_ballot"),
    # agm_egm
    (r"\b(annual general meeting|extraordinary general meeting|agm|egm|notice of agm|proceedings of agm)\b", "agm_egm"),
    # pledging
    (r"\b(pledge of shares|release of pledge|encumbrance|sast regulation 31)\b", "pledging"),
    # press_release
    (r"\b(press release|media release|product launch|partnership agreement|mou|memorandum of understanding)\b", "press_release"),
    # unclassified
    (r"\b(regulation 74\(5\)|duplicate share|loss of share certificate|esop allotment|compliance certificate)\b", "unclassified")
]

class AnnouncementClassifier:
    def classify(self, headline: str, raw_text: str = "") -> str:
        text = f"{headline} {raw_text}".lower()
        
        # Check rule match
        for pattern, category in KEYWORD_CATEGORY_RULES:
            if re.search(pattern, text):
                return category
                
        return "unclassified"

classifier = AnnouncementClassifier()
