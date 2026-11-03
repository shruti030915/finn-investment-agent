import re
from typing import List, Dict, Any

class FinancialChunker:
    def chunk_page(
        self,
        doc_name: str,
        page_number: int,
        ticker: str,
        page_text: str,
        max_chunk_chars: int = 500,
        overlap_chars: int = 80
    ) -> List[Dict[str, Any]]:
        """
        Splits page text into semantically cohesive financial chunks
        while preserving strict source document and page number metadata.
        """
        chunks = []
        # First try splitting by double-newlines (natural paragraphs)
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", page_text) if p.strip()]

        current_buf = ""
        chunk_idx = 1

        for p in paragraphs:
            if len(current_buf) + len(p) <= max_chunk_chars:
                current_buf = f"{current_buf}\n{p}".strip()
            else:
                if current_buf:
                    chunks.append({
                        "chunk_id": f"{doc_name}-p{page_number}-c{chunk_idx}",
                        "doc_name": doc_name,
                        "page_number": page_number,
                        "ticker": ticker.upper(),
                        "text": current_buf,
                        "snippet": current_buf[:150] + "..." if len(current_buf) > 150 else current_buf
                    })
                    chunk_idx += 1
                current_buf = p

        if current_buf:
            chunks.append({
                "chunk_id": f"{doc_name}-p{page_number}-c{chunk_idx}",
                "doc_name": doc_name,
                "page_number": page_number,
                "ticker": ticker.upper(),
                "text": current_buf,
                "snippet": current_buf[:150] + "..." if len(current_buf) > 150 else current_buf
            })

        return chunks

chunker = FinancialChunker()
