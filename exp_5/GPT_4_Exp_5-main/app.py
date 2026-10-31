import os
import re
from pathlib import Path
from datetime import datetime
import streamlit as st
import ollama
from pypdf import PdfReader

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
FALLBACK_MODELS = [MODEL_NAME, "llama3.2", "llama3.2:latest", "llama3.2:3b", "qwen2.5:3b"]

# ==============================================================================
# STREAMLIT CONFIG & CUSTOM STYLING
# ==============================================================================
st.set_page_config(
    page_title="LexiGuard AI — Automated Legal Contract & Risk Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.3px;
    }
    
    .legal-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 24px 30px;
        border-radius: 14px;
        margin-bottom: 24px;
        border-left: 6px solid #d97706;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .legal-banner h1 {
        font-size: 26px;
        margin: 0 0 6px 0;
        color: #ffffff;
    }
    
    .legal-banner p {
        font-size: 13.5px;
        color: #94a3b8;
        margin: 0;
    }
    
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    
    .sample-pill {
        display: inline-block;
        background: #eff6ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# SAMPLE CONTRACT PRESETS
# ==============================================================================
SAMPLE_CONTRACTS = {
    "None (Upload or Paste Custom Document)": "",
    "Mutual Non-Disclosure Agreement (NDA)": """MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of October 15, 2026 ("Effective Date"), by and between Apex Dynamics Inc., a Delaware corporation ("Apex"), and Horizon AI Solutions LLC, a California limited liability company ("Horizon").

1. Purpose. The parties wish to explore a potential business relationship concerning AI infrastructure and algorithmic acceleration ("Purpose").
2. Confidential Information. "Confidential Information" refers to any proprietary information, technical data, trade secrets, software architecture, or customer lists disclosed by either party to the other.
3. Obligations. Each party agrees to retain the Confidential Information in strict confidence and use at least the same degree of care as it uses for its own confidential information of like nature, but no less than reasonable care. Neither party shall reverse engineer or decompile any software shared.
4. Term and Termination. This Agreement shall remain in effect for a term of two (2) years from the Effective Date. The confidentiality obligations herein shall survive for three (3) years following termination.
5. Remedies. The parties acknowledge that any breach of this Agreement may cause irreparable harm for which damages may not be adequate, and the Disclosing Party shall be entitled to seek injunctive relief without posting a bond.
6. Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to conflict of law principles.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.""",
    "SaaS Master Services Agreement (MSA)": """MASTER SERVICES AGREEMENT (SaaS)

Effective Date: September 1, 2026.
Provider: CloudScale Enterprise Systems Inc. ("Provider")
Customer: Global FinTech Logistics Corp. ("Customer")

1. Services & SLA. Provider agrees to deliver enterprise cloud analytics services with a target uptime commitment of 99.9% ("SLA").
2. Fees & Payment. Customer shall pay $12,500 monthly in advance. Invoices are due Net 30 days. Late payments accrue interest at 1.5% per month.
3. Data Ownership & Security. Customer retains all rights, title, and interest in and to Customer Data. Provider shall maintain SOC 2 Type II compliance and AES-256 encryption at rest.
4. Limitation of Liability. EXCEPT FOR INDEMNIFICATION OBLIGATIONS OR GROSS NEGLIGENCE, NEITHER PARTY'S AGGREGATE LIABILITY SHALL EXCEED THE TOTAL FEES PAID IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.
5. Term and Termination. The initial term is twelve (12) months. Either party may terminate with 60 days' written notice prior to renewal, or immediately upon material breach uncured within 30 days.
6. Jurisdiction. The courts of New York County, New York, shall have exclusive jurisdiction."""
}


def read_document(uploaded_file):
    filename = uploaded_file.name.lower()
    if filename.endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="replace")
    if filename.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError("Please upload a TXT or PDF file.")


def preprocess_text(text):
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def analyze_document(document_text):
    prompt = f"""You are LexiGuard AI, an expert corporate legal counsel and contract review analyst.
Analyze the provided legal document and produce a rigorous, structured audit report.

Your report must contain the following 11 sections:
1. Document Type & Governing Jurisdiction
2. Identified Parties & Roles
3. Underlying Purpose & Recitals
4. Executive Summary of Terms
5. Core Mutual Obligations & Deliverables
6. Financial & Payment Terms (Amounts, schedules, late penalties)
7. Term, Effective Date & Duration
8. Termination Conditions & Notice Periods
9. Key Deadlines & Milestone Dates
10. Critical Clauses (Indemnity, Liability Caps, IP Ownership, Confidentiality)
11. Potential Legal Risks, Ambiguities, or Unbalanced Terms

Rules:
- Base your analysis solely on the text provided.
- If a section is unmentioned in the text, explicitly state: "Not specified in document".
- Provide objective, highly actionable legal risk commentary.

LEGAL DOCUMENT TEXT:
<document>
{document_text}
</document>"""

    last_error = None
    for model in dict.fromkeys(FALLBACK_MODELS):
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a meticulous contract audit assistant. Output clean, well-formatted markdown."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.2}
            )
            content = response.get("message", {}).get("content", "").strip()
            if content:
                return content
        except Exception as e:
            last_error = e
            if "not found" in str(e).lower():
                continue
            raise
    raise last_error or RuntimeError("Could not connect to Ollama.")


# ==============================================================================
# UI HEADER & SIDEBAR
# ==============================================================================
st.markdown("""
<div class="legal-banner">
    <h1>⚖️ LexiGuard AI — Automated Legal Document & Risk Analyzer</h1>
    <p>Upload or paste commercial agreements, NDAs, and service contracts for instant 11-point structural extraction and risk auditing powered by local LLMs.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("⚙️ System Status")
    st.success("🟢 Local AI Engine Active (Ollama)")
    st.caption(f"Default Model: `{MODEL_NAME}`")
    
    st.markdown("---")
    st.subheader("⚠️ Legal Compliance Notice")
    st.warning(
        "LexiGuard AI provides informational and structural review assistance. "
        "It does not constitute binding legal counsel. Always consult a licensed attorney."
    )
    
    st.markdown("---")
    st.caption("Experiment 5 • Building Applications using GPT-4 / LLMs")


# ==============================================================================
# INPUT SECTION
# ==============================================================================
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("1. Ingest Contract")
    sample_choice = st.selectbox("⚡ Or Select a Sample Contract Preset:", list(SAMPLE_CONTRACTS.keys()))
    
    uploaded_file = st.file_uploader("Upload Legal Agreement (PDF or TXT)", type=["txt", "pdf"])
    
    initial_text = SAMPLE_CONTRACTS.get(sample_choice, "")
    typed_text = st.text_area("Or Paste Custom Contract Text:", value=initial_text, height=220)

document_text = ""
if uploaded_file is not None:
    try:
        document_text = read_document(uploaded_file)
        source_name = uploaded_file.name
    except Exception as err:
        st.error(f"Error reading file: {err}")
        source_name = "Uploaded file"
elif typed_text.strip():
    document_text = typed_text.strip()
    source_name = sample_choice if sample_choice != "None (Upload or Paste Custom Document)" else "Pasted Contract"
else:
    source_name = "None"

with col2:
    st.subheader("2. Text Normalization & Inspection")
    if document_text:
        cleaned_text = preprocess_text(document_text)
        word_count = len(re.findall(r"\b\w+\b", cleaned_text))
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Character Count", len(cleaned_text))
        m2.metric("Word Count", word_count)
        m3.metric("Source", source_name[:15] + "..." if len(source_name) > 15 else source_name)
        
        st.text_area("Sanitized Preview", value=cleaned_text[:600] + ("..." if len(cleaned_text) > 600 else ""), height=150, disabled=True)
        
        if st.button("🚀 Run Comprehensive Legal Audit", type="primary", use_container_width=True):
            with st.spinner("Analyzing contract clauses, liabilities, and potential ambiguities with local AI..."):
                try:
                    report = analyze_document(cleaned_text)
                    st.session_state["legal_report"] = report
                    st.session_state["report_source"] = source_name
                    st.success("Legal analysis audit completed successfully!")
                except Exception as err:
                    st.error(f"Analysis failed: {err}. Ensure Ollama is running (`ollama serve`).")
    else:
        st.info("Select a sample contract above or upload a PDF/TXT document to begin.")


# ==============================================================================
# AUDIT REPORT DISPLAY
# ==============================================================================
if st.session_state.get("legal_report"):
    st.markdown("---")
    st.subheader("3. Comprehensive Legal Audit Report")
    
    report_text = st.session_state["legal_report"]
    source = st.session_state.get("report_source", "Contract")
    
    tab_report, tab_qa, tab_export = st.tabs(["📑 Structured Audit Breakdown", "💬 Interactive Contract Q&A", "📥 Export & Save"])
    
    with tab_report:
        st.markdown(report_text)
        
    with tab_qa:
        st.caption("Ask specific questions regarding this agreement (e.g., 'What is the indemnity cap?', 'Can they terminate without cause?')")
        user_q = st.text_input("Ask a question about this contract:")
        if user_q and st.button("Query Agreement"):
            with st.spinner("Searching contract terms..."):
                try:
                    qa_prompt = f"Based ONLY on this contract text, answer the following question clearly and concisely:\n\nCONTRACT:\n{document_text}\n\nQUESTION: {user_q}"
                    ans = ollama.chat(
                        model=resolve_model() if 'resolve_model' in globals() else MODEL_NAME,
                        messages=[{"role": "user", "content": qa_prompt}]
                    )
                    st.markdown(f"**Answer:** {ans.get('message', {}).get('content', '')}")
                except Exception as e:
                    st.error(f"Q&A error: {e}")
                    
    with tab_export:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"legal_audit_{timestamp}.md"
        
        st.download_button(
            label="📥 Download Markdown Report (.md)",
            data=report_text,
            file_name=export_filename,
            mime="text/markdown",
            use_container_width=True
        )
        
        save_path = OUTPUT_DIR / f"legal_analysis_{timestamp}.txt"
        if st.button("Save to Server Disk (outputs/)", use_container_width=True):
            save_path.write_text(report_text, encoding="utf-8")
            st.success(f"Report saved to `{save_path}`")
