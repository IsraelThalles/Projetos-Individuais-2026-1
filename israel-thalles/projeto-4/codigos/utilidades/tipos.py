from typing import Any, Literal, NamedTuple


class Documento(NamedTuple):
    hash: str
    publicador: str
    ano: int
    trimestre: int
    nome_arquivo: str
    caminho_local: str
    data_ingestao: str
    status_processamento: str

    @classmethod
    def from_row(cls, row: Any) -> "Documento":
        """Cria uma instância de Documento a partir de uma linha do banco de dados."""
        return cls(
            hash=row["hash"],
            publicador=row["publicador"],
            ano=row["ano"],
            trimestre=row["trimestre"],
            nome_arquivo=row["nome_arquivo"],
            caminho_local=row["caminho_local"],
            data_ingestao=row["data_ingestao"],
            status_processamento=row["status_processamento"]
        )
    
ESTADO_DO_PROCESSAMENTO = Literal['CONCLUÍDO', 'PENDENTE', 'ERRO']