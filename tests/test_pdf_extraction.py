import os
import unittest
from backend.config import PRIMARY_DOCS_DIR
from backend.pdf_extractor import pdf_extractor
from backend.chunking import chunker

class TestPDFExtractionAndChunking(unittest.TestCase):
    def test_pdf_extraction_page_count_and_text(self):
        pdf_path = os.path.join(PRIMARY_DOCS_DIR, "TCS_Q2_FY25_Earnings_Call_Transcript.pdf")
        self.assertTrue(os.path.exists(pdf_path), "Seed PDF should exist")

        pages = pdf_extractor.extract_pages(pdf_path)
        self.assertEqual(len(pages), 3, "TCS concall should have 3 pages")

        for p in pages:
            self.assertIn("doc_name", p)
            self.assertIn("page_number", p)
            self.assertGreater(p["char_count"], 100)
            self.assertIn("Tata Consultancy Services", p["text"] + pages[0]["text"])

    def test_chunking_preserves_metadata(self):
        chunks = chunker.chunk_page(
            doc_name="Test_Doc.pdf",
            page_number=2,
            ticker="TCS",
            page_text="Operating margin expanded 40 bps. Free cash flow was INR 11,261 crore."
        )
        self.assertGreater(len(chunks), 0)
        c = chunks[0]
        self.assertEqual(c["doc_name"], "Test_Doc.pdf")
        self.assertEqual(c["page_number"], 2)
        self.assertEqual(c["ticker"], "TCS")
        self.assertIn("margin", c["text"])

if __name__ == '__main__':
    unittest.main()
