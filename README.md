# 📄 AI Resume Verifier

An AI-powered resume analysis web application that compares a resume with a target job description and provides an estimated semantic match score, skill analysis, keyword gaps, and improvement suggestions.

## 🚀 Features

- Upload resumes in **PDF, DOCX, or TXT** format
- Paste a target job description
- Semantic similarity using **Sentence Transformers**
- Resume skill detection
- Job-description skill detection
- Matching keyword analysis
- Potential missing keyword identification
- Resume improvement suggestions
- Simple Streamlit web interface
- Runs locally without requiring an external API key

## 🧠 How It Works

The application follows this pipeline:

```text
Resume
  ↓
Text Extraction
  ↓
Text Cleaning
  ↓
Sentence Transformer Embeddings
  ↓
Semantic Similarity Score
  ↓
Skill + Keyword Analysis
  ↓
Improvement Suggestions
```

### Semantic Matching

The project uses the `all-MiniLM-L6-v2` Sentence Transformer model to convert the resume and job description into numerical embeddings. Cosine similarity is then used to estimate how closely the two texts match in meaning.

### Skill Analysis

The application also checks for commonly used technical skills such as:

- Python
- Java
- SQL
- Machine Learning
- Artificial Intelligence
- NLP
- Computer Vision
- OpenCV
- YOLO
- Qiskit
- Generative AI
- Git/GitHub
- Cloud technologies
- Streamlit
- Selenium

The skill dictionary can be extended in `app.py`.

## 🛠️ Tech Stack

- Python
- Streamlit
- Sentence Transformers
- PyTorch
- PyPDF
- python-docx
- Regular Expressions

## 📂 Project Structure

```text
AI_Resume_Verifier/
│
├── app.py
├── requirements.txt
└── README.md
```

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/AI-Resume-Verifier.git
cd AI-Resume-Verifier
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 📌 Example Use Case

A student applies for a Python/AI internship.

The student uploads their resume and pastes the internship's job description.

The application reports:

- Semantic match percentage
- Skills detected in the resume
- Skills detected in the job description
- Matching keywords
- Potential missing keywords
- Suggestions for improving the resume

## 🔮 Future Enhancements

- ATS-style section detection
- Resume section classification
- Experience and education extraction
- Named Entity Recognition
- Job-role classification
- Multiple job-description comparison
- Resume PDF report generation
- Interactive skill-gap dashboard
- Support for more languages
- Optional LLM-based personalized suggestions

## ⚠️ Disclaimer

This project is intended for educational and portfolio purposes. The generated percentage is an estimated semantic similarity score and is **not an official ATS score or a hiring decision**.

## 👩‍💻 Author

**Sai Shruthi V**

Computer Science & Engineering

---

⭐ If this project helped you learn something about NLP and AI, consider starring the repository.
