import unittest
from backend.announcement_classifier import classifier
from backend.priority_engine import priority_engine

class TestAnnouncementClassifierAndPriority(unittest.TestCase):
    def test_results_classification(self):
        headline = "Outcome of Board Meeting: Audited Financial Results for Q2 FY25"
        cat = classifier.classify(headline)
        self.assertEqual(cat, "results")
        prio = priority_engine.determine_priority(cat, headline)
        self.assertEqual(prio, "HIGH")

    def test_management_change_classification(self):
        headline = "Intimation of Appointment of Chief Financial Officer under Reg 30"
        cat = classifier.classify(headline)
        self.assertEqual(cat, "management_change")
        prio = priority_engine.determine_priority(cat, headline)
        self.assertEqual(prio, "HIGH")

    def test_dividend_classification(self):
        headline = "Declaration of Interim Dividend of Rs 6.25 per Equity Share"
        cat = classifier.classify(headline)
        self.assertEqual(cat, "dividend")
        prio = priority_engine.determine_priority(cat, headline)
        self.assertEqual(prio, "MEDIUM")

    def test_unclassified_routine_compliance(self):
        headline = "Certificate under Regulation 74(5) of SEBI (DP) Regulations"
        cat = classifier.classify(headline)
        self.assertEqual(cat, "unclassified")
        prio = priority_engine.determine_priority(cat, headline)
        self.assertEqual(prio, "LOW")

    def test_management_enrichment_extracts_details(self):
        headline = "Appointment of Mr. Vikram Singh as Chief Financial Officer"
        enrichment = priority_engine.enrich_announcement("management_change", headline, "")
        self.assertIsNotNone(enrichment)
        self.assertIn("Vikram Singh", enrichment.get("executive_name", ""))
        self.assertIn("Chief Financial Officer", enrichment.get("role", ""))

if __name__ == '__main__':
    unittest.main()

