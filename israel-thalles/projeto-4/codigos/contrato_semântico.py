from pydantic import BaseModel, Field
from typing import List, Literal, Optional



class MetricaOperacional(BaseModel):
    """Representa uma métrica operacional ou financeira extraída do relatório, com seu nome, valor, unidade e categoria."""
    categoria: Literal["Lançamentos", "Vendas", "Financeiro", "Estoque", "Produção", "Outros"] = Field(
        description="Classifique a métrica na macro-categoria que melhor a representa."
    )
    empresa_referencia: str = Field(
        description="A qual construtora esta métrica pertence. Ex: MRV, Cury, Tenda, Direcional. Se for um dado geral da própria empresa do relatório, use o nome dela."
    )
    nome_metrica: str = Field(
        description="Nome da métrica encontrada. Ex: Lançamentos (VGV), Vendas Líquidas, Banco de Terrenos, Unidades Produzidas, Geração de Caixa."
    )
    valor: Optional[float] = Field(
        default=None,
        description="O valor numérico extraído. Pode ser o número absoluto bruto ou a variação percentual (ex: -32.0, 14.0)."
    )
    unidade_medida: Optional[str] = Field(
        default=None,
        description="A unidade do valor absoluto. Ex: 'R$', 'US$', 'unidades', '%', 'm²' etc."
    )



class RelatorioConjuntura(BaseModel):
    """Representa o relatório de conjuntura extraído do texto, contendo o nome do publicador, ano, trimestre e a lista de métricas operacionais e financeiras extraídas."""
    publicador: str = Field(
        description="Nome do publicador do relatório. Ex: MRV, Cury, Tenda, Plano e Plano, Boletim de Conjuntura."
    )
    ano: int = Field(
        description="Ano do relatório com 4 dígitos. Ex: 2026."
    )
    trimestre: int = Field(
        description="Trimestre do relatório. Ex: 1, 2, 3 ou 4."
    )
    metricas: List[MetricaOperacional] = Field(
        description="Lista de todas as métricas operacionais e financeiras extraídas do texto."
    )