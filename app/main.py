# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    TextoEntrada,
    SentimentoSaida,
    TextoLoteEntrada,
    SentimentoLoteSaida,
    SentimentoLoteItem,
    EstatisticasLote,
)
from app.services.sentiment import classificar_sentimento, classificar_lote


app = FastAPI(
    title="API de Análise de Sentimentos de Feedbacks",
    description="Recebe textos (comentários, avaliações, tweets) e retorna o sentimento.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # em produção você pode restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "API de Análise de Sentimentos está funcionando.",
        "docs_url": "/docs",
        "health_url": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/sentimento", response_model=SentimentoSaida)
def analisar_sentimento(entrada: TextoEntrada):
    """
    Analisa o sentimento de um único texto.

    Você pode escolher o modo:
      - 'triclasse' (padrão): positivo / neutro / negativo
      - 'binario' : positivo / negativo
    """
    resultado = classificar_sentimento(entrada.texto, modo=entrada.modo or "triclasse")
    return resultado


@app.post("/sentimentos/lote", response_model=SentimentoLoteSaida)
def analisar_sentimento_lote(entrada: TextoLoteEntrada):
    """
    Analisa o sentimento de vários textos de uma vez e retorna
    também estatísticas agregadas (útil para medir satisfação ao longo do tempo).
    """
    resultados_brutos = classificar_lote(entrada.textos, modo=entrada.modo or "triclasse")

    itens: list[SentimentoLoteItem] = []
    positivos = negativos = neutros = 0

    for texto, res in zip(entrada.textos, resultados_brutos):
        label = res["label"]
        score = res["score"]

        if label == "positivo":
            positivos += 1
        elif label == "negativo":
            negativos += 1
        else:
            neutros += 1

        itens.append(
            SentimentoLoteItem(
                texto=texto,
                label=label,
                score=score,
            )
        )

    total = len(entrada.textos) if entrada.textos else 0

    estat = EstatisticasLote(
        total=total,
        positivos=positivos,
        negativos=negativos,
        neutros=neutros,
        porcent_positivos=(positivos / total * 100) if total else 0.0,
        porcent_negativos=(negativos / total * 100) if total else 0.0,
        porcent_neutros=(neutros / total * 100) if total else 0.0,
    )

    return SentimentoLoteSaida(
        resultados=itens,
        estatisticas=estat,
    )
