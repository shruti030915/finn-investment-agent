import unittest
from backend.financial_analyzer import financial_analyzer
from backend.models import ResearchQueryRequest
from backend.stock_data import stock_manager
from backend.alert_engine import alert_engine
from backend.announcement_fetcher import announcement_manager

class TestEnhancedResearchQuality(unittest.TestCase):
    def setUp(self):
        self.req = ResearchQueryRequest(ticker="TCS", query="Analyze financial trajectory and guidance vs actuals")
        self.res = financial_analyzer.analyze_company(self.req)

    def test_section_specific_retrieval_no_repetition(self):
        """ISSUE 1: Verify Business Snapshot, Trajectory, Balance Sheet, and Cash Quality are distinct."""
        biz = self.res.business_snapshot.content
        traj = self.res.financial_trajectory.content
        fin = self.res.financial_snapshot.content
        bs = self.res.balance_sheet_leverage.content
        cash = self.res.cash_quality_conversion.content

        # 1. Business Snapshot vs Trajectory
        self.assertNotEqual(biz, traj)
        self.assertIn("BFSI", biz)
        self.assertIn("Energy", biz)
        self.assertIn("Total Contract Value", biz)

        # 2. Balance Sheet vs Financial Snapshot
        self.assertNotEqual(bs, fin)
        self.assertIn("Debt-to-Equity", bs)
        self.assertIn("43,892", bs)

        # 3. Cash Quality vs Trajectory & Balance Sheet
        self.assertNotEqual(cash, traj)
        self.assertNotEqual(cash, bs)
        self.assertIn("operating cash flow", cash.lower())
        self.assertIn("11,261", cash)

    def test_financial_metric_extraction_and_provenance(self):
        """ISSUE 2: Metric provenance, no zero substitution, distinct EBITDA vs EBIT."""
        self.assertGreater(len(self.res.all_metrics_provenance), 0)
        
        found_metrics = {m.metric_name: m for m in self.res.all_metrics_provenance}
        
        # Check provenance fields
        rev = found_metrics.get("Revenue from Operations")
        self.assertIsNotNone(rev)
        self.assertEqual(rev.value, "INR 64,259 Cr")
        self.assertEqual(rev.unit, "INR Crore")
        self.assertEqual(rev.period, "Q2 FY25")
        self.assertEqual(rev.page_number, 2)
        self.assertEqual(rev.figure_type, "Reported")

        # Operating margin vs EBITDA margin
        op_margin = found_metrics.get("Operating Margin (EBIT Margin)")
        self.assertEqual(op_margin.value, "24.1%")
        self.assertIn("EBIT / Revenue", op_margin.formula)

        ebitda_margin = found_metrics.get("EBITDA Margin")
        self.assertIn("Not disclosed separately", ebitda_margin.value)

        # Missing data not represented as zero
        total_assets = found_metrics.get("Total Assets")
        self.assertIsNotNone(total_assets)
        self.assertEqual(total_assets.value, "Not disclosed in indexed documents")
        self.assertNotEqual(total_assets.value, "0")
        self.assertNotEqual(total_assets.value, "0.0")

    def test_financial_trajectory_comparison_math(self):
        """ISSUE 3: Trajectory table and trend chart with mathematically verified growth."""
        self.assertGreater(len(self.res.trajectory_table), 0)
        table_map = {row.metric: row for row in self.res.trajectory_table}
        
        # Verify Revenue YoY and QoQ
        rev_row = table_map.get("Revenue from Operations (INR Cr)")
        self.assertIsNotNone(rev_row)
        self.assertEqual(rev_row.yoy_growth, "+7.6%")
        self.assertEqual(rev_row.qoq_growth, "+2.63%")

        # Verify Operating Profit YoY and QoQ
        ebit_row = table_map.get("Operating Profit / EBIT (INR Cr)")
        self.assertIsNotNone(ebit_row)
        self.assertEqual(ebit_row.yoy_growth, "+6.9%")
        self.assertEqual(ebit_row.qoq_growth, "+0.27%")

        # Verify Trend Chart points
        self.assertEqual(len(self.res.trajectory_chart), 3)
        p_q2_25 = [p for p in self.res.trajectory_chart if p.period == "Q2 FY25"][0]
        self.assertEqual(p_q2_25.revenue_cr, 64259.0)
        self.assertEqual(p_q2_25.ebit_cr, 15486.0)

    def test_cash_quality_comparison(self):
        """ISSUE 4: Cash quality comparison between PAT, OCF, and FCF."""
        comp = self.res.cash_comparison
        self.assertIsNotNone(comp)
        self.assertEqual(comp.pat_value, "INR 11,909 Cr")
        self.assertEqual(comp.ocf_value, "INR 11,261 Cr")
        self.assertEqual(comp.fcf_value, "INR 11,261 Cr")
        self.assertIn("100.2%", comp.conversion_ratio)
        self.assertIn("94.56%", comp.conversion_ratio)
        self.assertIn("Exceptional quality of earnings", comp.assessment)

    def test_citations_contributed_to_sections(self):
        """ISSUE 5: Cited documents actually contributed to the relevant section."""
        self.assertGreater(len(self.res.all_cited_sources), 0)
        for s in self.res.all_cited_sources:
            self.assertEqual(s.ticker, "TCS")
            self.assertIn("TCS_Q2_FY25", s.doc_id)
            self.assertIn(s.page_number, [1, 2, 3])

    def test_executive_summary_present(self):
        """Verify Executive Summary synthesizes headline results and health."""
        self.assertIsNotNone(self.res.executive_summary)
        self.assertIn("Tata Consultancy Services", self.res.executive_summary.content)
        self.assertIn("64,259", self.res.executive_summary.content)
        self.assertIn("24.1%", self.res.executive_summary.content)

    def test_unindexed_ticker_titan_safety(self):
        """Verify unindexed ticker TITAN receives clean warning with zero fabricated figures."""
        req_titan = ResearchQueryRequest(ticker="TITAN", query="guidance and margins")
        res_titan = financial_analyzer.analyze_company(req_titan)
        self.assertFalse(res_titan.grounded_in_primary_sources)
        self.assertEqual(len(res_titan.all_cited_sources), 0)
        self.assertGreater(len(res_titan.missing_data_disclosures), 0)
        self.assertIn("No primary annual report or concall PDF is currently indexed for TITAN", res_titan.missing_data_disclosures[0])

    def test_push_functionality_intact(self):
        """ISSUE 7: Existing Push functionality remains intact."""
        summary = stock_manager.get_portfolio_summary()
        self.assertEqual(summary.stock_count, 18)
        self.assertEqual(summary.total_value_inr, 8193516.0)
        self.assertEqual(summary.total_pnl_inr, 666716.0)
        self.assertEqual(summary.total_pnl_pct, 8.86)

        alerts = alert_engine.evaluate_alerts()
        self.assertGreater(len(alerts), 0)

        announcements = announcement_manager.get_announcements()
        self.assertGreater(len(announcements), 0)

if __name__ == '__main__':
    unittest.main()
