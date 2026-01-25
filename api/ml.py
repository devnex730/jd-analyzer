from .models import JDmodel
from asgiref.sync import sync_to_async
from sklearn.feature_extraction.text import TfidfVectorizer
import asyncio

Vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=3,
    max_df=0.85,
    max_features=3000,
)

_model_trained = False
_train_lock = asyncio.Lock()


def get_jd_corpus():
    return list(JDmodel.objects.values_list("text", flat=True))


async def train_once():
    global _model_trained

    if _model_trained:
        return

    async with _train_lock:
        if _model_trained:
            return

        corpus = await sync_to_async(get_jd_corpus)()

        Vectorizer.fit(corpus)

        _model_trained = True

        print(f"✅ Model trained on {len(corpus)} JDs")
