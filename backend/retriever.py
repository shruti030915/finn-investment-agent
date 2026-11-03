import math
import re
import logging
from typing import List, Dict, Any
from backend.document_fetcher import document_fetcher
from backend.models import DocumentSourceItem

logger = logging.getLogger("finn.retriever")

def tokenize(text: str) -> List[str]:
    return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_]{2,}\b", text)]

class PurePythonTFIDFRetriever:
    """
    High-performance, pure-Python TF-IDF and Cosine Similarity vector retriever.
    Zero external C-library dependencies (avoids Windows scipy DLL permission issues),
    100% deterministic and auditable for financial compliance.
    """
    def retrieve(self, ticker: str, query: str, top_k: int = 5) -> List[DocumentSourceItem]:
        chunks = document_fetcher.get_chunks_for_ticker(ticker)
        if not chunks:
            logger.warning(f"No chunks found for ticker {ticker}")
            return []

        # Tokenize corpus
        docs_tokens = [tokenize(c["text"]) for c in chunks]
        query_tokens = tokenize(query)
        num_docs = len(docs_tokens)

        if not query_tokens or num_docs == 0:
            return [
                DocumentSourceItem(
                    doc_id=c["doc_name"],
                    title=c["doc_name"].replace(".pdf", "").replace("_", " "),
                    ticker=c["ticker"],
                    doc_type=document_fetcher._infer_doc_type(c["doc_name"]),
                    page_number=c["page_number"],
                    relevance_score=0.5,
                    snippet=c["snippet"]
                )
                for c in chunks[:top_k]
            ]

        # Calculate Document Frequencies (DF)
        df: Dict[str, int] = {}
        for doc in docs_tokens:
            unique_terms = set(doc)
            for t in unique_terms:
                df[t] = df.get(t, 0) + 1

        # Calculate IDF with smoothing
        idf = {t: math.log((num_docs + 1) / (count + 1)) + 1.0 for t, count in df.items()}
        default_idf = math.log(num_docs + 1) + 1.0

        # Query vector
        q_tf: Dict[str, float] = {}
        for t in query_tokens:
            q_tf[t] = q_tf.get(t, 0.0) + 1.0
        q_len = len(query_tokens)
        q_vec = {t: (count / q_len) * idf.get(t, default_idf) for t, count in q_tf.items()}
        q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0

        # Score each document chunk
        scored_chunks = []
        for idx, (doc, chunk) in enumerate(zip(docs_tokens, chunks)):
            d_len = len(doc) or 1
            d_tf: Dict[str, float] = {}
            for t in doc:
                d_tf[t] = d_tf.get(t, 0.0) + 1.0

            dot_product = 0.0
            d_sq_sum = 0.0
            for t, count in d_tf.items():
                w = (count / d_len) * idf.get(t, default_idf)
                d_sq_sum += w * w
                if t in q_vec:
                    dot_product += w * q_vec[t]

            d_norm = math.sqrt(d_sq_sum) or 1.0
            score = dot_product / (q_norm * d_norm)
            scored_chunks.append((score, chunk))

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        results: List[DocumentSourceItem] = []
        for score, chunk in scored_chunks[:top_k]:
            results.append(DocumentSourceItem(
                doc_id=chunk["doc_name"],
                title=chunk["doc_name"].replace(".pdf", "").replace("_", " "),
                ticker=chunk["ticker"],
                doc_type=document_fetcher._infer_doc_type(chunk["doc_name"]),
                page_number=chunk["page_number"],
                relevance_score=round(float(score), 4),
                snippet=chunk["snippet"]
            ))

        return results

    def score_chunks(self, chunks: List[Dict[str, Any]], query: str) -> List[Any]:
        """Directly scores a specific list of chunks against a targeted query string."""
        if not chunks:
            return []
        docs_tokens = [tokenize(c["text"]) for c in chunks]
        query_tokens = tokenize(query)
        num_docs = len(docs_tokens)
        if not query_tokens or num_docs == 0:
            return [(0.5, c) for c in chunks]

        df: Dict[str, int] = {}
        for doc in docs_tokens:
            for t in set(doc):
                df[t] = df.get(t, 0) + 1

        idf = {t: math.log((num_docs + 1) / (count + 1)) + 1.0 for t, count in df.items()}
        default_idf = math.log(num_docs + 1) + 1.0

        q_tf: Dict[str, float] = {}
        for t in query_tokens:
            q_tf[t] = q_tf.get(t, 0.0) + 1.0
        q_len = len(query_tokens)
        q_vec = {t: (count / q_len) * idf.get(t, default_idf) for t, count in q_tf.items()}
        q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0

        scored = []
        for doc, chunk in zip(docs_tokens, chunks):
            d_len = len(doc) or 1
            d_tf: Dict[str, float] = {}
            for t in doc:
                d_tf[t] = d_tf.get(t, 0.0) + 1.0

            dot_product = 0.0
            d_sq_sum = 0.0
            for t, count in d_tf.items():
                w = (count / d_len) * idf.get(t, default_idf)
                d_sq_sum += w * w
                if t in q_vec:
                    dot_product += w * q_vec[t]

            d_norm = math.sqrt(d_sq_sum) or 1.0
            score = dot_product / (q_norm * d_norm)
            scored.append((float(score), chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored

retriever = PurePythonTFIDFRetriever()
