# app/services/model_loader.py
from functools import lru_cache

from transformers import pipeline


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    """
    Carrega o pipeline de análise de sentimento uma única vez.

    Usa um modelo multilíngue pré-treinado (inclui português).
    Na primeira vez que rodar, ele vai baixar os pesos da internet.
    """
    clf = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment"
    )
    return clf
