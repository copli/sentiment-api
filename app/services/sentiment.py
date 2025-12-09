# app/services/sentiment.py
from typing import Literal, TypedDict, List

from app.services.model_loader import get_sentiment_pipeline

SentimentLabel = Literal["positivo", "negativo", "neutro"]


class SentimentResult(TypedDict):
    label: SentimentLabel
    score: float  # confiança entre 0 e 1


def _map_model_output_to_label(model_label: str) -> SentimentLabel:
    """
    Adapta o rótulo do modelo para nosso padrão: positivo / neutro / negativo.

    O modelo 'nlptown/bert-base-multilingual-uncased-sentiment'
    devolve algo como: '1 star', '2 stars', ..., '5 stars'.
    """
    label = model_label.lower()

    if "1 star" in label or "2 star" in label:
        return "negativo"
    if "3 star" in label:
        return "neutro"
    if "4 star" in label or "5 star" in label:
        return "positivo"

    # fallback genérico
    return "neutro"


def classificar_sentimento(texto: str, modo: str = "triclasse") -> SentimentResult:
    """
    Usa o modelo de NLP para classificar o sentimento do texto.

    modo:
        - "triclasse": retorna positivo / neutro / negativo
        - "binario": retorna apenas positivo / negativo
    """
    clf = get_sentiment_pipeline()

    # Saída típica do pipeline:
    # [{"label": "5 stars", "score": 0.85}]
    raw = clf(texto)[0]

    label_modelo = raw["label"]
    score_modelo = float(raw["score"])

    label_triclasse = _map_model_output_to_label(label_modelo)

    # Se o modo for binário, convertemos neutro para positivo/negativo
    if modo == "binario":
        if label_triclasse == "neutro":
            label_binario: SentimentLabel = "positivo" if score_modelo >= 0.5 else "negativo"
            return {
                "label": label_binario,
                "score": score_modelo,
            }
        else:
            return {
                "label": label_triclasse,
                "score": score_modelo,
            }

    # modo padrão: triclasse
    return {
        "label": label_triclasse,
        "score": score_modelo,
    }


def classificar_lote(textos: List[str], modo: str = "triclasse") -> List[SentimentResult]:
    """
    Classifica uma lista de textos de uma vez.
    Retorna a lista de resultados no mesmo formato da função simples.
    """
    clf = get_sentiment_pipeline()

    # pipeline aceita lista de textos
    raw_results = clf(textos)

    resultados: List[SentimentResult] = []

    for raw in raw_results:
        label_modelo = raw["label"]
        score_modelo = float(raw["score"])
        label_triclasse = _map_model_output_to_label(label_modelo)

        if modo == "binario":
            if label_triclasse == "neutro":
                label_binario: SentimentLabel = (
                    "positivo" if score_modelo >= 0.5 else "negativo"
                )
                resultados.append(
                    {
                        "label": label_binario,
                        "score": score_modelo,
                    }
                )
            else:
                resultados.append(
                    {
                        "label": label_triclasse,
                        "score": score_modelo,
                    }
                )
        else:
            resultados.append(
                {
                    "label": label_triclasse,
                    "score": score_modelo,
                }
            )

    return resultados
