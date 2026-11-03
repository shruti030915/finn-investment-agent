import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from backend.config import DEFAULT_PRICE_MOVE_THRESHOLD, DEFAULT_VOLUME_MULT_THRESHOLD, DEFAULT_DIGEST_WINDOW_HOURS, DEFAULT_MONITORED_CATEGORIES
from backend.models import Alert, AlertSettings
from backend.stock_data import stock_manager
from backend.announcement_fetcher import announcement_manager

logger = logging.getLogger("finn.alerts")

class AlertEngine:
    def __init__(self):
        self.settings = AlertSettings(
            price_move_threshold=DEFAULT_PRICE_MOVE_THRESHOLD,
            volume_mult_threshold=DEFAULT_VOLUME_MULT_THRESHOLD,
            digest_window_hours=DEFAULT_DIGEST_WINDOW_HOURS,
            monitored_categories=DEFAULT_MONITORED_CATEGORIES
        )
        self.acknowledged_ids = set()

    def update_settings(self, new_settings: AlertSettings):
        self.settings = new_settings
        logger.info(f"Updated alert settings: Price={self.settings.price_move_threshold}%, Vol={self.settings.volume_mult_threshold}x")

    def get_settings(self) -> AlertSettings:
        return self.settings

    def evaluate_alerts(self) -> List[Alert]:
        alerts: List[Alert] = []

        # 1. Evaluate EOD Stock Price & Volume Triggers
        stocks = stock_manager.get_all_portfolio_stocks()
        for s in stocks:
            # Price Trigger
            if abs(s.change_pct) >= self.settings.price_move_threshold:
                direction = "Surge" if s.change_pct > 0 else "Drop"
                alert_id = f"ALT-PRC-{s.ticker}"
                alerts.append(Alert(
                    id=alert_id,
                    ticker=s.ticker,
                    company_name=s.name,
                    timestamp=datetime.now().isoformat(),
                    alert_type="PRICE_MOVE",
                    priority="HIGH" if abs(s.change_pct) >= 4.0 else "MEDIUM",
                    title=f"Significant Price {direction}: {s.change_pct:+.2f}%",
                    description=f"{s.ticker} traded at INR {s.price:,.2f} ({s.change_pct:+.2f}%), breaching user threshold of ±{self.settings.price_move_threshold}%.",
                    metric_value=s.change_pct,
                    threshold_value=self.settings.price_move_threshold,
                    details={"price": s.price, "prev_close": s.prev_close, "change": s.change},
                    acknowledged=(alert_id in self.acknowledged_ids)
                ))

            # Volume Trigger
            if s.volume_multiple >= self.settings.volume_mult_threshold:
                alert_id = f"ALT-VOL-{s.ticker}"
                alerts.append(Alert(
                    id=alert_id,
                    ticker=s.ticker,
                    company_name=s.name,
                    timestamp=datetime.now().isoformat(),
                    alert_type="UNUSUAL_VOLUME",
                    priority="HIGH" if s.volume_multiple >= 2.5 else "MEDIUM",
                    title=f"Unusual Volume Surge: {s.volume_multiple:.2f}x 20-Day Average",
                    description=f"Traded volume {s.volume:,} shares crossed {s.volume_multiple:.1f}x the 20-day historical average of {s.avg_volume_20d:,} shares.",
                    metric_value=s.volume_multiple,
                    threshold_value=self.settings.volume_mult_threshold,
                    details={"volume": s.volume, "avg_volume_20d": s.avg_volume_20d},
                    acknowledged=(alert_id in self.acknowledged_ids)
                ))

        # 2. Evaluate Corporate Announcement Triggers
        announcements = announcement_manager.get_announcements(window_hours=self.settings.digest_window_hours)
        for ann in announcements:
            if ann.category in self.settings.monitored_categories and ann.priority in ["HIGH", "MEDIUM"]:
                alert_id = f"ALT-ANN-{ann.id}"
                alerts.append(Alert(
                    id=alert_id,
                    ticker=ann.ticker,
                    company_name=ann.company_name,
                    timestamp=ann.timestamp,
                    alert_type="MATERIAL_ANNOUNCEMENT",
                    priority=ann.priority,
                    title=f"Material Filing ({ann.category.upper()}): {ann.headline[:65]}...",
                    description=ann.raw_text[:160] + "...",
                    metric_value=None,
                    threshold_value=None,
                    details={"category": ann.category, "source": ann.source, "announcement_id": ann.id},
                    acknowledged=(alert_id in self.acknowledged_ids)
                ))

        # Sort: unacknowledged first, then HIGH priority first, then timestamp
        prio_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        alerts.sort(key=lambda a: (a.acknowledged, prio_order.get(a.priority, 3), a.timestamp), reverse=False)
        return alerts

    def acknowledge_alert(self, alert_id: str):
        self.acknowledged_ids.add(alert_id)
        return {"status": "ok", "alert_id": alert_id, "acknowledged": True}

alert_engine = AlertEngine()
