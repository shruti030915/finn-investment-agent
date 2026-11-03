import os
import fitz  # PyMuPDF
from typing import List, Dict, Any

class PDFExtractor:
    def extract_pages(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extracts text from each page using PyMuPDF (fitz),
        preserving document name, 1-based page numbers, and character count.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        doc_name = os.path.basename(pdf_path)
        doc = fitz.open(pdf_path)
        pages_data = []

        for page_idx, page in enumerate(doc):
            text = page.get_text("text")
            pages_data.append({
                "doc_name": doc_name,
                "file_path": pdf_path,
                "page_number": page_idx + 1,  # 1-based indexing for financial citations
                "char_count": len(text),
                "text": text.strip()
            })

        doc.close()
        return pages_data

pdf_extractor = PDFExtractor()

