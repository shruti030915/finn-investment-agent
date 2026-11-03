import os
import io
import unittest
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

from backend.document_fetcher import document_fetcher
from backend.financial_analyzer import financial_analyzer
from backend.models import ResearchQueryRequest
from backend.config import PRIMARY_DOCS_DIR

class TestPDFUploadPipeline(unittest.TestCase):
    def setUp(self):
        self.test_filename = "INFY_Q2_FY25_RESULTS.pdf"
        self.test_path = os.path.join(PRIMARY_DOCS_DIR, self.test_filename)
        # Ensure clean state before test
        for p in [self.test_path, os.path.join(PRIMARY_DOCS_DIR, "INFY_INFOSYS_TEST_FY25_RESULTS.pdf")]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
        document_fetcher.index_primary_documents()

    def tearDown(self):
        if os.path.exists(self.test_path):
            try:
                os.remove(self.test_path)
                document_fetcher.index_primary_documents()
            except Exception:
                pass
        # Clean any INFY_ prefixed test artifacts
        for p in [os.path.join(PRIMARY_DOCS_DIR, "INFY_INFOSYS_TEST_FY25_RESULTS.pdf")]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                    document_fetcher.index_primary_documents()
                except Exception:
                    pass

    def _create_sample_pdf_bytes(self):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Infosys Limited — Q2 FY25 Financial Disclosures", styles['Heading1']),
            Paragraph("Revenues grew 5.1% YoY to INR 40,986 crore. Operating margin was 21.1%. Free cash flow reached INR 8,394 crore.", styles['Normal']),
            PageBreak(),
            Paragraph("Management Guidance vs Actual Execution", styles['Heading2']),
            Paragraph("Full-year FY25 revenue growth guidance revised upwards to 3.75%-4.50% in constant currency. Margin band retained at 20-22%.", styles['Normal']),
            Paragraph("Bull Thesis: Large deal TCV of $2.4B and upward guidance revision. Bear Thesis: Discretionary transformation spend moderation.", styles['Normal'])
        ]
        doc.build(story)
        buf.seek(0)
        return buf.read()

    def test_upload_and_immediate_rag_indexing(self):
        # 1. Before upload: verify INFY is ungrounded
        req_before = ResearchQueryRequest(ticker="INFY", query="guidance and margins")
        res_before = financial_analyzer.analyze_company(req_before)
        self.assertFalse(res_before.grounded_in_primary_sources, "INFY should not be grounded before indexing")

        # 2. Upload / Index PDF via save_and_index_pdf
        pdf_bytes = self._create_sample_pdf_bytes()
        res_upload = document_fetcher.save_and_index_pdf(
            filename=self.test_filename,
            pdf_bytes=pdf_bytes,
            ticker="INFY"
        )
        
        self.assertEqual(res_upload["status"], "success")
        self.assertEqual(res_upload["ticker"], "INFY")
        self.assertTrue(os.path.exists(self.test_path))

        # 3. After upload: verify immediate dynamic RAG grounding
        req_after = ResearchQueryRequest(ticker="INFY", query="guidance and margins")
        res_after = financial_analyzer.analyze_company(req_after)
        
        self.assertTrue(res_after.grounded_in_primary_sources, "INFY must now be grounded in the uploaded PDF")
        self.assertGreater(len(res_after.all_cited_sources), 0)
        self.assertEqual(res_after.all_cited_sources[0].doc_id, self.test_filename)
        self.assertIn("INFY", res_after.ticker)
        
        # Verify page retrieval
        page_doc = document_fetcher.get_document_page(self.test_filename, 1)
        self.assertIsNotNone(page_doc)
        self.assertIn("Infosys Limited", page_doc["text"])

        print(f"\n[UPLOAD PIPELINE PASSED] Successfully uploaded {self.test_filename}, indexed 2 pages via PyMuPDF, and executed grounded RAG research citing Page {res_after.all_cited_sources[0].page_number}.")

if __name__ == '__main__':
    unittest.main()
