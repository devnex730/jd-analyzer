from .models import JDmodel
from sklearn.feature_extraction.text import TfidfVectorizer

jd_corpus = list(JDmodel.objects.values_list("text", flat=True))

Vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2),
    min_df=3,
    max_df=0.85,
    max_features=3000,
)
def train():
    Vectorizer.fit(jd_corpus)
    return f"model is traind on {len(jd_corpus)} JDs"