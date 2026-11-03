import os
import glob
import logging
from typing import List, Dict, Any, Optional
from backend.config import PRIMARY_DOCS_DIR
from backend.pdf_extractor import pdf_extractor
from backend.chunking import chunker

logger = logging.getLogger("finn.documents")

class DocumentFetcher:
    def __init__(self):
        self._documents: List[Dict[str, Any]] = []
        self._all_chunks: List[Dict[str, Any]] = []
        self.index_primary_documents()

    def _infer_ticker(self, filename: str) -> str:
        upper = filename.upper()
        known = ["TCS", "RELIANCE", "HDFCBANK", "INFY", "WIPRO", "TATAMOTORS", "ICICIBANK", "SBIN", "ITC", "LT", "SUNPHARMA"]
        for k in known:
            if k in upper:
                return k
        return "GENERAL"

    def _infer_doc_type(self, filename: str) -> str:
        upper = filename.upper()
        if "EARNINGS" in upper or "TRANSCRIPT" in upper or "CONCALL" in upper:
            return "earnings_transcript"
        elif "ANNUAL" in upper or "AR" in upper:
            return "annual_report"
        elif "RESULTS" in upper or "FINANCIAL" in upper:
            return "results_filing"
        elif "PRESENTATION" in upper or "INVESTOR" in upper:
            return "presentation"
        return "filing"

    def index_primary_documents(self):
        pdf_files = glob.glob(os.path.join(PRIMARY_DOCS_DIR, "*.pdf"))
        self._documents = []
        self._all_chunks = []

        for fpath in pdf_files:
            fname = os.path.basename(fpath)
            ticker = self._infer_ticker(fname)
            doc_type = self._infer_doc_type(fname)

            try:
                pages = pdf_extractor.extract_pages(fpath)
                doc_entry = {
                    "doc_id": fname,
                    "title": fname.replace(".pdf", "").replace("_", " "),
                    "ticker": ticker,
                    "doc_type": doc_type,
                    "file_path": fpath,
                    "page_count": len(pages),
                    "pages": pages
                }
                self._documents.append(doc_entry)

                for p in pages:
                    p_chunks = chunker.chunk_page(
                        doc_name=fname,
                        page_number=p["page_number"],
                        ticker=ticker,
                        page_text=p["text"]
                    )
                    self._all_chunks.extend(p_chunks)

            except Exception as e:
                logger.error(f"Failed to index PDF {fname}: {e}")

        logger.info(f"Indexed {len(self._documents)} documents with {len(self._all_chunks)} chunks.")

    def get_documents_for_ticker(self, ticker: str) -> List[Dict[str, Any]]:
        clean = ticker.upper().replace(".NS", "")
        return [d for d in self._documents if d["ticker"] == clean or d["ticker"] == "GENERAL"]

    def get_chunks_for_ticker(self, ticker: str) -> List[Dict[str, Any]]:
        clean = ticker.upper().replace(".NS", "")
        matches = [c for c in self._all_chunks if c["ticker"] == clean]
        if not matches:
            # If no specific company docs, return all chunks as broader corpus
            matches = self._all_chunks
        return matches

    def get_all_chunks(self) -> List[Dict[str, Any]]:
        return self._all_chunks

    def get_document_page(self, doc_id: str, page_number: int) -> Optional[Dict[str, Any]]:
        for d in self._documents:
            if d["doc_id"] == doc_id:
                for p in d["pages"]:
                    if p["page_number"] == page_number:
                        return p
        return None

    def save_and_index_pdf(self, filename: str, pdf_bytes: bytes, ticker: Optional[str] = None) -> Dict[str, Any]:
        target_filename = filename or f"{ticker.upper() if ticker else 'DOCUMENT'}_Uploaded.pdf"
        if ticker and ticker.upper() not in target_filename.upper():
            target_filename = f"{ticker.upper()}_{target_filename}"
        if not target_filename.lower().endswith(".pdf"):
            target_filename += ".pdf"
        
        save_path = os.path.join(PRIMARY_DOCS_DIR, target_filename)
        with open(save_path, "wb") as f:
            f.write(pdf_bytes)
        
        self.index_primary_documents()
        inferred_ticker = self._infer_ticker(target_filename)
        return {
            "status": "success",
            "doc_id": target_filename,
            "ticker": inferred_ticker,
            "message": f"Successfully indexed primary document {target_filename}. Ready for immediate RAG research."
        }

document_fetcher = DocumentFetcher()

