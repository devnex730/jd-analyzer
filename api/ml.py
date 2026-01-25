from .models import JDmodel
from asgiref.sync import sync_to_async
from sklearn.feature_extraction.text import TfidfVectorizer

Vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=3,
    max_df=0.85,
    max_features=3000,
)

def get_jd_corpus():
    return list(JDmodel.objects.values_list("text", flat=True))

async def get_jd_corpus_async():
    return await sync_to_async(get_jd_corpus)()

async def train():
    corpus = await get_jd_corpus_async()
    Vectorizer.fit(corpus)
    return f"Model trained on {len(corpus)} JDs"
