from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def compute_match(jd, resumes):
    data = [jd] + resumes
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(data)

    jd_vector = matrix[0]
    resume_vectors = matrix[1:]

    scores = cosine_similarity(jd_vector, resume_vectors)[0]

    return scores


def get_keywords(text):
    try:
        tfidf = TfidfVectorizer(stop_words="english")
        matrix = tfidf.fit_transform([text])
        names = tfidf.get_feature_names_out()

        indices = matrix[0].toarray()[0].argsort()[-5:][::-1]
        top_words = [names[i] for i in indices]
        return top_words
    except:
        return []


def get_contact_info(text):
    email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phone = re.findall(r"(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", text)

    return {
        "email": email[0] if email else "N/A",
        "phone": phone[0] if phone else "N/A",
    }
