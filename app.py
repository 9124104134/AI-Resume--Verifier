import re
from pathlib import Path

import streamlit as st
from pypdf import PdfReader
from docx import Document
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="AI Resume Verifier", page_icon="📄", layout="wide")

MODEL_NAME = "all-MiniLM-L6-v2"

@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

def extract_pdf(file):
    reader = PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text(file):
    suffix = Path(file.name).suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(file)
    if suffix == ".docx":
        return extract_docx(file)
    if suffix == ".txt":
        return file.read().decode("utf-8", errors="ignore")
    raise ValueError("Unsupported file format. Use PDF, DOCX, or TXT.")

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def tokenize(text):
    return set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-]*", text.lower()))

COMMON_SKILLS = {
    "python", "java", "c", "c++", "javascript", "typescript", "html", "css",
    "sql", "mysql", "postgresql", "mongodb", "git", "github", "docker",
    "aws", "azure", "gcp", "google cloud", "machine learning", "deep learning",
    "artificial intelligence", "nlp", "computer vision", "opencv", "yolo",
    "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy", "qiskit",
    "streamlit", "flask", "django", "fastapi", "rest api", "api", "kafka",
    "selenium", "javafx", "power bi", "excel", "data analysis", "data analytics",
    "generative ai", "llm", "rag", "langchain", "prompt engineering"
}

def find_skills(text):
    lower = text.lower()
    found = []
    for skill in sorted(COMMON_SKILLS, key=len, reverse=True):
        if re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", lower):
            found.append(skill)
    return sorted(set(found))

def get_keyword_gaps(resume, job_description):
    resume_words = tokenize(resume)
    jd_words = tokenize(job_description)
    ignored = {
        "the", "and", "for", "with", "from", "that", "this", "your", "you",
        "are", "will", "our", "have", "has", "into", "using", "use", "role",
        "job", "work", "team", "years", "year", "skills", "experience"
    }
    keywords = {w for w in jd_words if len(w) >= 3 and w not in ignored}
    matched = sorted(keywords & resume_words)
    missing = sorted(keywords - resume_words)
    return matched, missing

def semantic_score(resume, job_description):
    model = load_model()
    embeddings = model.encode(
        [clean_text(resume), clean_text(job_description)],
        convert_to_tensor=True,
        normalize_embeddings=True
    )
    score = float(util.cos_sim(embeddings[0], embeddings[1]).item())
    return max(0.0, min(100.0, score * 100))

def generate_suggestions(resume_skills, jd_skills, missing_keywords):
    suggestions = []
    missing_skills = [s for s in jd_skills if s not in resume_skills]
    if missing_skills:
        suggestions.append(
            "Consider adding relevant skills you genuinely possess: "
            + ", ".join(missing_skills[:8]) + "."
        )
    if missing_keywords:
        suggestions.append(
            "Review the job description for important terms such as: "
            + ", ".join(missing_keywords[:10]) + "."
        )
    if len(resume_skills) < 5:
        suggestions.append(
            "Add a clear Technical Skills section with the tools and technologies you actually use."
        )
    suggestions.append(
        "Use measurable achievements in project and internship bullets, such as percentages, counts, time saved, or accuracy."
    )
    suggestions.append(
        "Tailor the summary and project descriptions to the target role without adding skills you do not have."
    )
    return suggestions

st.title("📄 AI Resume Verifier")
st.write("Compare a resume with a target job description using semantic similarity and skill/keyword analysis.")

with st.sidebar:
    st.header("How it works")
    st.markdown(
        """
        1. Upload a resume.
        2. Paste the target job description.
        3. The app extracts text.
        4. A Sentence Transformer compares semantic meaning.
        5. Skills and keywords are compared.
        6. Suggestions are generated.
        """
    )

resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX, TXT"
)

job_description = st.text_area(
    "Paste Job Description",
    height=280,
    placeholder="Paste the complete job description here..."
)

if st.button("🔍 Verify Resume", type="primary"):
    if not resume_file:
        st.error("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    try:
        resume_text = extract_text(resume_file)
        if len(resume_text.strip()) < 50:
            st.error("Not enough readable text was found in the resume.")
            st.stop()

        with st.spinner("Analyzing resume..."):
            resume_text = clean_text(resume_text)
            jd_text = clean_text(job_description)

            score = semantic_score(resume_text, jd_text)
            resume_skills = find_skills(resume_text)
            jd_skills = find_skills(jd_text)
            matched_keywords, missing_keywords = get_keyword_gaps(resume_text, jd_text)
            suggestions = generate_suggestions(
                resume_skills, jd_skills, missing_keywords
            )

        st.success("Resume analysis completed.")

        c1, c2, c3 = st.columns(3)
        c1.metric("Semantic Match", f"{score:.1f}%")
        c2.metric("Matched Keywords", len(matched_keywords))
        c3.metric("Detected Resume Skills", len(resume_skills))

        st.subheader("📊 Match Interpretation")
        if score >= 80:
            st.success("Strong semantic alignment with the target role.")
        elif score >= 65:
            st.info("Good alignment, but the resume can be tailored further.")
        elif score >= 50:
            st.warning("Moderate alignment. Review missing skills and keywords.")
        else:
            st.error("Low alignment. Consider tailoring the resume to the role.")

        left, right = st.columns(2)

        with left:
            st.subheader("✅ Skills Found in Resume")
            st.write(", ".join(resume_skills) if resume_skills else "No skills detected.")

            st.subheader("🔑 Keywords Found")
            st.write(", ".join(matched_keywords[:40]) if matched_keywords else "No matching keywords detected.")

        with right:
            st.subheader("🎯 Skills Mentioned in Job Description")
            st.write(", ".join(jd_skills) if jd_skills else "No predefined skills detected.")

            st.subheader("⚠️ Potential Missing Keywords")
            st.write(", ".join(missing_keywords[:40]) if missing_keywords else "No major keyword gaps detected.")

        st.subheader("💡 Resume Improvement Suggestions")
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")

        st.caption(
            "This tool is an assistive resume-analysis project. Its score is not an official ATS score "
            "and should not be treated as a hiring decision."
        )

    except Exception as exc:
        st.error(f"Could not analyze the file: {exc}")
