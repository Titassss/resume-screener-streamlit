import streamlit as st
from resume_parser import get_file_content
from matcher import compute_match, get_keywords, get_contact_info

st.set_page_config(page_title="Resume Screener", layout="wide")

st.markdown(
    """
<style>
    .stTextArea>div>div>textarea { background-color: #2b2b2b; color: white; }
    .stTextInput>div>div>input { background-color: #2b2b2b; color: white; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("AI Resume Screener")
st.text("An AI tool to rank resumes based on job description")

with st.sidebar:
    st.header("Upload Files")
    uploaded = st.file_uploader(
        "Choose PDF or TXT files", type=["pdf", "txt"], accept_multiple_files=True
    )

st.subheader("Job Description")
jd = st.text_area("Enter JD here...", height=300)

if st.button("Start Analysis"):
    if not jd or not uploaded:
        st.warning("Please upload files and enter a JD.")
    else:
        with st.spinner("Processing..."):
            texts = []
            files_data = []

            for f in uploaded:
                txt = get_file_content(f)
                if not txt.strip():
                    continue

                texts.append(txt)
                info = get_contact_info(txt)
                files_data.append(
                    {
                        "name": f.name,
                        "text": txt,
                        "email": info["email"],
                        "phone": info["phone"],
                    }
                )

            if texts:
                scores = compute_match(jd, texts)

               
                results = sorted(
                    zip(scores, files_data), key=lambda x: x[0], reverse=True
                )

                st.success("Done!")
                st.write("---")

                for score, data in results:
                    keys = get_keywords(data["text"])

                    with st.expander(f"{data['name']} - Score: {score*100:.2f}%"):
                        c1, c2 = st.columns(2)
                        c1.metric("Match", f"{score*100:.2f}%")
                        c2.write(f"Email: {data['email']}")
                        c2.write(f"Phone: {data['phone']}")
                        st.write("Keywords: " + ", ".join(keys))
