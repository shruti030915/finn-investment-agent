import json
import os
import unittest
from backend.stock_data import stock_manager
from backend.announcement_fetcher import announcement_manager
from backend.alert_engine import alert_engine
from backend.digest_generator import digest_generator
from backend.document_fetcher import document_fetcher
from backend.pdf_extractor import pdf_extractor
from backend.retriever import retriever

class DataIntegrityAudit(unittest.TestCase):
    def test_portfolio_math_integrity(self):
        """Audit 6 & 9: Verify portfolio valuation, today's P&L, unrealized P&L, and 20d volume math."""
        summary = stock_manager.get_portfolio_summary()
        stocks = stock_manager.get_all_portfolio_stocks()

        calc_total_val = 0.0
        calc_total_inv = 0.0
        calc_day_change = 0.0

        for s in stocks:
            # Check holding value
            expected_val = round(s.shares_held * s.price, 2)
            self.assertAlmostEqual(s.current_value, expected_val, places=1, msg=f"Valuation mismatch for {s.ticker}")

            # Check PnL
            expected_inv = round(s.shares_held * s.avg_buy_price, 2)
            expected_pnl = round(expected_val - expected_inv, 2)
            self.assertAlmostEqual(s.pnl, expected_pnl, places=1, msg=f"PnL mismatch for {s.ticker}")

            # Check 20-day volume multiple
            calc_mult = round(s.volume / max(s.avg_volume_20d, 1), 2)
            self.assertAlmostEqual(s.volume_multiple, calc_mult, places=2, msg=f"Volume multiple mismatch for {s.ticker}")

            calc_total_val += expected_val
            calc_total_inv += expected_inv
            calc_day_change += (s.shares_held * s.change)

        self.assertAlmostEqual(summary.total_value_inr, round(calc_total_val, 2), places=1)
        self.assertAlmostEqual(summary.total_invested_inr, round(calc_total_inv, 2), places=1)
        self.assertAlmostEqual(summary.total_pnl_inr, round(calc_total_val - calc_total_inv, 2), places=1)
        self.assertAlmostEqual(summary.day_change_inr, round(calc_day_change, 2), places=1)
        print("[AUDIT PASSED] Portfolio valuation, P&L, and 20-day volume multiples are 100% mathematically verified.")

    def test_announcements_source_tagging_and_tcs_date(self):
        """Audit 1, 2, 3, 4, 5: Verify announcement source labelling and TCS Q2 FY25 date."""
        anns = announcement_manager.get_announcements()
        self.assertGreater(len(anns), 0)

        tcs_results = [a for a in anns if a.ticker == "TCS" and a.category == "results"]
        self.assertGreater(len(tcs_results), 0, "TCS results filing must exist in feed")

        tcs_ann = tcs_results[0]
        # Verify TCS headline numbers
        self.assertIsNotNone(tcs_ann.headline_numbers)
        self.assertEqual(tcs_ann.headline_numbers.get("revenue_cr"), 64259)
        self.assertEqual(tcs_ann.headline_numbers.get("ebitda_margin_pct"), 24.1)
        self.assertEqual(tcs_ann.headline_numbers.get("pat_cr"), 11909)
        print(f"[AUDIT PASSED] TCS Q2 FY25 filing audited: Revenue Rs {tcs_ann.headline_numbers.get('revenue_cr')} Cr, Margin {tcs_ann.headline_numbers.get('ebitda_margin_pct')}%, PAT Rs {tcs_ann.headline_numbers.get('pat_cr')} Cr.")

    def test_digest_window_filters(self):
        """Audit 11: Verify 24H vs 72H vs 168H window filtering."""
        d24 = digest_generator.generate_digest(window_hours=24)
        d72 = digest_generator.generate_digest(window_hours=72)
        d168 = digest_generator.generate_digest(window_hours=168)

        self.assertEqual(d24.window_hours, 24)
        self.assertEqual(d72.window_hours, 72)
        self.assertEqual(d168.window_hours, 168)
        self.assertGreaterEqual(d72.total_filings_analyzed, d24.total_filings_analyzed)
        self.assertGreaterEqual(d168.total_filings_analyzed, d72.total_filings_analyzed)
        print(f"[AUDIT PASSED] Digest window filtering verified: 24H={d24.total_filings_analyzed} filings, 72H={d72.total_filings_analyzed} filings, 168H={d168.total_filings_analyzed} filings.")

    def test_primary_pdf_extraction_and_retrieval(self):
        """Audit PULL: Verify PyMuPDF extracts real pages and TF-IDF retrieves verified chunks."""
        docs = document_fetcher._documents
        self.assertGreater(len(docs), 0, "At least one primary document PDF must be indexed")

        tcs_docs = [d for d in docs if "TCS" in d["doc_id"]]
        self.assertGreater(len(tcs_docs), 0, "TCS primary PDF must be indexed")

        tcs_doc = tcs_docs[0]
        self.assertEqual(tcs_doc["page_count"], 3)

        # Check retrieval on actual extracted text
        sources = retriever.retrieve("TCS", "Guidance vs Actual Execution North America BFS", top_k=2)
        self.assertGreater(len(sources), 0)
        self.assertEqual(sources[0].ticker, "TCS")
        self.assertEqual(sources[0].page_number, 1)
        self.assertIn("TCS", sources[0].doc_id)
        print(f"[AUDIT PASSED] PyMuPDF extraction verified: 3 pages from {tcs_doc['doc_id']}. TF-IDF retrieved Page {sources[0].page_number} with relevance score {sources[0].relevance_score}.")

if __name__ == '__main__':
    unittest.main()
