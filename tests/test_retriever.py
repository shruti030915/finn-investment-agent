import unittest
from backend.retriever import retriever
from backend.financial_analyzer import financial_analyzer
from backend.models import ResearchQueryRequest

class TestRetrieverAndAnalyzer(unittest.TestCase):
    def test_pure_python_retrieval(self):
        sources = retriever.retrieve(ticker="TCS", query="EBITDA operating margin cash flow", top_k=3)
        self.assertGreater(len(sources), 0)
        top_source = sources[0]
        self.assertEqual(top_source.ticker, "TCS")
        self.assertGreaterEqual(top_source.page_number, 1)
        self.assertGreaterEqual(top_source.relevance_score, 0.0)

    def test_grounded_financial_research(self):
        req = ResearchQueryRequest(ticker="TCS", query="Narrative vs numbers and guidance delivery")
        res = financial_analyzer.analyze_company(req)
        self.assertEqual(res.ticker, "TCS")
        self.assertTrue(res.grounded_in_primary_sources)
        self.assertIsNotNone(res.narrative_vs_numbers)
        self.assertIn("Guidance", res.narrative_vs_numbers.content)
        self.assertIn("Execution", res.narrative_vs_numbers.content)
        self.assertGreater(len(res.all_cited_sources), 0)

if __name__ == '__main__':
    unittest.main()

