import unittest
from backend.alert_engine import alert_engine
from backend.models import AlertSettings

class TestAlertEngine(unittest.TestCase):
    def test_default_threshold_evaluation(self):
        alerts = alert_engine.evaluate_alerts()
        self.assertGreater(len(alerts), 0)

        # Check for price alerts
        price_alerts = [a for a in alerts if a.alert_type == "PRICE_MOVE"]
        self.assertGreater(len(price_alerts), 0)

        # Check for volume alerts
        vol_alerts = [a for a in alerts if a.alert_type == "UNUSUAL_VOLUME"]
        self.assertGreater(len(vol_alerts), 0)

    def test_configurable_threshold_behavior(self):
        # Set ultra-high price threshold of 10%
        original_settings = alert_engine.get_settings()
        alert_engine.update_settings(AlertSettings(
            price_move_threshold=10.0,
            volume_mult_threshold=5.0,
            digest_window_hours=24,
            monitored_categories=["results"]
        ))
        
        filtered_alerts = alert_engine.evaluate_alerts()
        price_alerts_at_10 = [a for a in filtered_alerts if a.alert_type == "PRICE_MOVE"]
        self.assertEqual(len(price_alerts_at_10), 0, "No stock moved > 10% in demo data")

        # Restore original settings
        alert_engine.update_settings(original_settings)

    def test_acknowledgement(self):
        alerts = alert_engine.evaluate_alerts()
        first_alert = alerts[0]
        alert_engine.acknowledge_alert(first_alert.id)
        self.assertIn(first_alert.id, alert_engine.acknowledged_ids)

if __name__ == '__main__':
    unittest.main()

