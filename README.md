# Resume Screener

This is a project to screen resumes using AI. It compares resumes with a job description and gives a match score.

## How to run

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Features
- Upload PDF or Text files
- Paste Job Description
- Get ranked results with score
- Shows contact info and keywords

## Libraries used
- Streamlit
- PyMuPDF (fitz)
- Tesseract (for OCR)
- Scikit-learn (TF-IDF)
