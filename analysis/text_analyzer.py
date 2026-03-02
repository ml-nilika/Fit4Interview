from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def analyze_answer(user_answer, ideal_answer):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([ideal_answer, user_answer])

    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    score = int(similarity * 100)

    return score
