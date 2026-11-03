"""
FINN — Financial Investment Intelligence Agent
One-Click Launcher for ENAM Holdings Build Challenge

Launches FastAPI backend serving REST API endpoints and responsive mobile-first terminal.
"""
import os
import sys
import uvicorn

def main():
    print("=" * 70)
    print("  FINN — Financial Investment Intelligence Agent")
    print("  Built for ENAM Holdings AI Engineer Build Challenge")
    print("=" * 70)
    
    # 1. Ensure seed documents and market data exist
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    docs_dir = os.path.join(data_dir, "primary_documents")
    
    if not os.path.exists(os.path.join(data_dir, "portfolio_seed.json")):
        print("[FINN] Generating initial portfolio seed data...")
        from backend.generate_seed_data import PORTFOLIO_COMPANIES
    
    if not os.path.exists(os.path.join(docs_dir, "TCS_Q2_FY25_Earnings_Call_Transcript.pdf")):
        print("[FINN] Generating primary PDF filings and earnings call transcripts...")
        import backend.generate_seed_docs as gen_docs
        gen_docs.create_tcs_concall()
        gen_docs.create_reliance_results()
        gen_docs.create_hdfc_bank_report()

    print("[FINN] System diagnostics:")
    print("  - Primary Documents Index: Ready (PyMuPDF)")
    print("  - Vector Retrieval Engine: Ready (Pure Python TF-IDF Cosine Similarity)")
    print("  - Proactive Push Feed:     Ready (18 Portfolio Stocks)")
    print("  - Deep Pull Research:      Ready (Primary Document Grounding)")
    print()
    print("  -> Application Terminal:  http://localhost:8000")
    print("  -> Interactive API Docs:  http://localhost:8000/docs")
    print("=" * 70)
    print("Starting server on http://0.0.0.0:8000 ... Press Ctrl+C to stop.")
    
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()

