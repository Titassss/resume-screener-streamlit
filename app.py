import streamlit as st
import pandas as pd
from resume_parser import extract_text
from matcher import calculate_similarity, get_top_keywords, extract_contact_info

st.set_page_config(page_title="Resume Screener", layout="wide")

st.markdown(
    """
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #2b2b2b;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #2b2b2b;
        color: white;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("AI Resume Screener")
st.markdown("### Intelligent Candidate Ranking & Analysis")

with st.sidebar:
    st.header("Upload Data")
    uploaded_files = st.file_uploader(
        "Upload Resumes (PDF/TXT)", type=["pdf", "txt"], accept_multiple_files=True
    )
    st.info(f"Loaded: {len(uploaded_files)} resumes")
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown(
        "1. Upload resumes.\n2. Paste job description.\n3. Get ranked list with insights."
    )

st.subheader("Job Description")
job_description = st.text_area("Paste the JD here...", height=300)

if st.button("Analyze Resumes", type="primary"):
    if not job_description:
        st.warning("Please enter a job description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Analyzing resumes..."):
            resume_texts = []
            resume_data = []

            for uploaded_file in uploaded_files:
                try:
                    text = extract_text(uploaded_file)

                    if not text.strip():
                        st.warning(f"Could not extract text from {uploaded_file.name}.")
                        continue

                    resume_texts.append(text)

                    contact = extract_contact_info(text)

                    resume_data.append(
                        {
                            "Filename": uploaded_file.name,
                            "Text": text,
                            "Email": contact["email"],
                            "Phone": contact["phone"],
                        }
                    )
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")

            if resume_texts:
                scores = calculate_similarity(job_description, resume_texts)

                ranked_indices = sorted(
                    range(len(scores)), key=lambda i: scores[i], reverse=True
                )

                st.success("Analysis Complete!")

                st.markdown("---")
                st.subheader("Ranked Candidates")

                for idx in ranked_indices:
                    score = scores[idx]
                    data = resume_data[idx]

                    keywords = get_top_keywords(data["Text"])

                    with st.expander(
                        f"#{ranked_indices.index(idx) + 1} - {data['Filename']} (Score: {score*100:.1f}%)"
                    ):
                        c1, c2, c3 = st.columns([1, 2, 2])

                        with c1:
                            st.metric("Match Score", f"{score*100:.1f}%")
                            if score > 0.7:
                                st.success("High Match")
                            elif score > 0.4:
                                st.warning("Medium Match")
                            else:
                                st.error("Low Match")

                        with c2:
                            st.markdown("**Contact Info:**")
                            st.write(f"Email: {data['Email']}")
                            st.write(f"Phone: {data['Phone']}")

                        with c3:
                            st.markdown("**Top Keywords Found:**")
                            st.write(", ".join(keywords))

                        st.text_area(
                            "Resume Preview", data["Text"][:500] + "...", height=100
                        )
            else:
                st.error("No valid text extracted from resumes.")

if not uploaded_files:
    st.info("Start by uploading resumes in the sidebar.")
