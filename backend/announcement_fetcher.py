import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional
from backend.config import DATA_DIR
from backend.models import Announcement
from backend.announcement_classifier import classifier
from backend.priority_engine import priority_engine

logger = logging.getLogger("finn.announcements")
SEED_ANNOUNCEMENTS_FILE = os.path.join(DATA_DIR, "announcements_seed.json")

class AnnouncementManager:
    def __init__(self):
        self._announcements: List[Announcement] = []
        self.load_seed()

    def load_seed(self):
        if os.path.exists(SEED_ANNOUNCEMENTS_FILE):
            try:
                with open(SEED_ANNOUNCEMENTS_FILE, "r", encoding="utf-8") as f:
                    raw_list = json.load(f)
                    self._announcements = []
                    for item in raw_list:
                        # Ensure category and priority are assigned
                        cat = item.get("category") or classifier.classify(item["headline"], item.get("raw_text", ""))
                        prio = item.get("priority") or priority_engine.determine_priority(cat, item["headline"], item.get("raw_text", ""))
                        enrich = priority_engine.enrich_announcement(cat, item["headline"], item.get("raw_text", ""), item.get("enrichment"))
                        
                        item["category"] = cat
                        item["priority"] = prio
                        item["enrichment"] = enrich
                        self._announcements.append(Announcement(**item))
                logger.info(f"Loaded {len(self._announcements)} announcements.")
            except Exception as e:
                logger.error(f"Error loading announcements seed: {e}")

    def get_announcements(
        self,
        ticker: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        window_hours: Optional[int] = None
    ) -> List[Announcement]:
        results = self._announcements

        if ticker:
            clean = ticker.upper().replace(".NS", "")
            results = [a for a in results if a.ticker.upper() == clean]

        if priority and priority.upper() != "ALL":
            results = [a for a in results if a.priority.upper() == priority.upper()]

        if category and category.lower() != "all":
            results = [a for a in results if a.category.lower() == category.lower()]

        if window_hours:
            cutoff = datetime.now() - timedelta(hours=window_hours)
            filtered = []
            for a in results:
                try:
                    dt = datetime.fromisoformat(a.timestamp)
                    if dt >= cutoff:
                        filtered.append(a)
                except Exception:
                    filtered.append(a)
            results = filtered

        # Sort descending by timestamp
        results = sorted(results, key=lambda a: a.timestamp, reverse=True)
        return results

    def add_announcement(self, data: dict) -> Announcement:
        cat = data.get("category") or classifier.classify(data.get("headline", ""), data.get("raw_text", ""))
        prio = data.get("priority") or priority_engine.determine_priority(cat, data.get("headline", ""), data.get("raw_text", ""))
        enrich = priority_engine.enrich_announcement(cat, data.get("headline", ""), data.get("raw_text", ""), data.get("enrichment"))
        
        ann = Announcement(
            id=data.get("id", f"ANN-{len(self._announcements)+1:03d}"),
            ticker=data.get("ticker", "UNKNOWN").upper(),
            company_name=data.get("company_name", data.get("ticker", "Company")),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            headline=data.get("headline", "Corporate Disclosure"),
            category=cat,
            priority=prio,
            source=data.get("source", "Exchange Regulatory Filing"),
            source_doc_url=data.get("source_doc_url"),
            raw_text=data.get("raw_text", ""),
            headline_numbers=data.get("headline_numbers"),
            enrichment=enrich
        )
        self._announcements.insert(0, ann)
        return ann

announcement_manager = AnnouncementManager()
