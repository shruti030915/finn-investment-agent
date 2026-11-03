import os
import unittest
from backend.stock_data import stock_manager
from backend.announcement_fetcher import announcement_manager
from backend.alert_engine import alert_engine
from backend.models import AlertSettings, ResearchQueryRequest
from backend.digest_generator import digest_generator
from backend.financial_analyzer import financial_analyzer
from backend.document_fetcher import document_fetcher

class TestInteractiveFeaturesAndAudit(unittest.TestCase):
    def test_navigation_and_portfolio_integrity(self):
        """Audit 6, 7, 8: Stock prices, volume, and portfolio valuation."""
        summary = stock_manager.get_portfolio_summary()
        self.assertEqual(summary.stock_count, 18)
        self.assertGreater(summary.total_value_inr, 0)
        
        # Verify 20d average volume math
        for s in summary.stocks:
            expected_mult = round(s.volume / max(s.avg_volume_20d, 1), 2)
            self.assertEqual(s.volume_multiple, expected_mult)

    def test_digest_window_filters(self):
        """Audit 11: 24H, 3D (72h), 7D (168h) filtering behavior."""
        d24 = digest_generator.generate_digest(window_hours=24)
        d72 = digest_generator.generate_digest(window_hours=72)
        d168 = digest_generator.generate_digest(window_hours=168)

        self.assertEqual(d24.window_hours, 24)
        self.assertEqual(d72.window_hours, 72)
        self.assertEqual(d168.window_hours, 168)
        # 24H should filter out filings older than 24h
        self.assertGreaterEqual(d72.total_filings_analyzed, d24.total_filings_analyzed)
        self.assertGreaterEqual(d168.total_filings_analyzed, d72.total_filings_analyzed)

    def test_alert_acknowledgement_and_thresholds(self):
        """Audit 12: Alert acknowledgement and threshold controls."""
        initial_alerts = alert_engine.evaluate_alerts()
        self.assertGreater(len(initial_alerts), 0)

        # Acknowledge first alert
        test_alert = initial_alerts[0]
        alert_engine.acknowledge_alert(test_alert.id)
        
        # Verify it is in acknowledged_ids
        self.assertIn(test_alert.id, alert_engine.acknowledged_ids)

        # Update thresholds
        orig = alert_engine.get_settings()
        alert_engine.update_settings(AlertSettings(
            price_move_threshold=5.0,
            volume_mult_threshold=3.0,
            digest_window_hours=24,
            monitored_categories=["results"]
        ))
        strict_alerts = alert_engine.evaluate_alerts()
        # Restoring
        alert_engine.update_settings(orig)

    def test_pull_research_pipeline_and_citations(self):
        """Audit PULL: Verify PyMuPDF extraction, TF-IDF retrieval, and financial analysis."""
        # 1. Test grounded company (TCS)
        req_tcs = ResearchQueryRequest(ticker="TCS", query="guidance vs actuals execution and margins")
        res_tcs = financial_analyzer.analyze_company(req_tcs)

        self.assertEqual(res_tcs.ticker, "TCS")
        self.assertTrue(res_tcs.grounded_in_primary_sources)
        self.assertGreater(len(res_tcs.all_cited_sources), 0)
        
        # Verify page numbers are 1-based integers
        for s in res_tcs.all_cited_sources:
            self.assertGreaterEqual(s.page_number, 1)
            self.assertTrue(s.doc_id.endswith(".pdf"))

        # Verify key metrics were dynamically extracted
        self.assertIn("Revenue_Q2_FY25", res_tcs.financial_snapshot.key_metrics)
        self.assertEqual(res_tcs.financial_snapshot.key_metrics["Revenue_Q2_FY25"], "INR 64,259 Cr")
        self.assertEqual(res_tcs.financial_snapshot.key_metrics["Operating_Margin"], "24.1%")

        # 2. Test ungrounded company (ZOMATO)
        req_zomato = ResearchQueryRequest(ticker="ZOMATO", query="financial trajectory")
        res_zomato = financial_analyzer.analyze_company(req_zomato)
        
        self.assertEqual(res_zomato.ticker, "ZOMATO")
        self.assertFalse(res_zomato.grounded_in_primary_sources)
        self.assertGreater(len(res_zomato.missing_data_disclosures), 0)
        self.assertEqual(len(res_zomato.all_cited_sources), 0)

if __name__ == '__main__':
    unittest.main()

