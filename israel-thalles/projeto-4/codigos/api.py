from typing import List, Optional
from fastapi import FastAPI, Query
from contrato_semântico import MetricaResposta, CATEGORIA
from utilidades.banco import buscar_metricas_operacionais_filtradas



# Cria a nossa API (o garçom)
app = FastAPI(
    title="API de Conjuntura Habitacional",
    description="Motor de extração de dados do setor imobiliário via LLM",
    version="1.0.0"
)

# Cria a rota (o menu) que o desafio exigiu
@app.get("/api/conjuntura", response_model=List[MetricaResposta])
def buscar_dados_conjuntura(
    empresa: Optional[str] = Query(None, description="Filtrar por construtora (ex: MRV, Cury)"),
    ano: Optional[int] = Query(None, description="Filtrar por ano do relatório (ex: 2025, 2026)"),
    trimestre: Optional[int] = Query(None, description="Filtrar por trimestre (1, 2, 3 ou 4)"),
    categoria: Optional[CATEGORIA] = Query(None, description="Filtrar por macro-categoria (ex: 'Lançamentos', 'Vendas', 'Produção')")
):
    """
    Retorna as métricas operacionais extraídas dos boletins e balanços,
    permitindo múltiplos cruzamentos e filtros.
    """
    
    metricas = buscar_metricas_operacionais_filtradas(empresa, ano, trimestre, categoria)

    # Garantir que metricas é iterável; quando None, retornar lista vazia
    return [dict(metrica) for metrica in metricas] if metricas else []