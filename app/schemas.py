# app/schemas.py
from typing import List

from pydantic import BaseModel


class TextoEntrada(BaseModel):
    texto: str
    modo: str | None = "triclasse"  # "triclasse" ou "binario"


class SentimentoSaida(BaseModel):
    label: str   # "positivo" | "negativo" | "neutro"
    score: float # confiança entre 0 e 1


class TextoLoteEntrada(BaseModel):
    textos: List[str]
    modo: str | None = "triclasse"


class SentimentoLoteItem(BaseModel):
    texto: str
    label: str
    score: float


class EstatisticasLote(BaseModel):
    total: int
    positivos: int
    negativos: int
    neutros: int
    porcent_positivos: float
    porcent_negativos: float
    porcent_neutros: float


class SentimentoLoteSaida(BaseModel):
    resultados: List[SentimentoLoteItem]
    estatisticas: EstatisticasLote
