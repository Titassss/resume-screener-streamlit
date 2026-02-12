# AI Resume Screening System

A robust, AI-powered tool to screen resumes against a job description. It uses **TF-IDF Vectorization** and **Cosine Similarity** to rank candidates, extracts keywords, and parses contact information.

## Features

-   **Multi-Format Support**: Handles PDF (native & scanned) and TXT files.
-   **Intelligent Parsing**: Uses `PyMuPDF` (fitz) for high-speed text extraction and OCR fallback.
-   **OCR Ready**: Automatically converts PDF pages to images for OCR (via `pytesseract`) if text extraction yields poor results.
-   **Advanced Matching**:
    -   Ranks candidates by relevance percentage.
    -   Extracts top keywords contributing to the match.
    -    parses Email and Phone Numbers.
-   **Beautiful UI**: Modern Streamlit interface with metrics, expandable details, and clean layout.

## Installation

1.  **Clone the repository**.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### OCR Prerequisites
To enable OCR for scanned PDFs:
1.  Install **Tesseract-OCR** on your system.
    -   **Windows**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
2.  Add Tesseract to your system PATH.

## Usage

1.  Run the application:
    ```bash
    streamlit run app.py
    ```
2.  **Upload Resumes**: Drag & drop multiple PDF or TXT files.
3.  **Paste Job Description**: Enter the job requirements.
4.  **Analyze**: Click "Analyze Resumes" to see the ranked dashboard.

## Project Structure
-   `app.py`: Main application with enhanced UI.
-   `resume_parser.py`: Robust parsing logic (PyMuPDF + OCR).
-   `matcher.py`: Similarity core + Keyword & Contact extraction.
-   `requirements.txt`: Python dependencies.
