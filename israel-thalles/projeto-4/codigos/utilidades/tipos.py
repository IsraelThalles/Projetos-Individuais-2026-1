from typing import Any, NamedTuple


class Documento(NamedTuple):
    hash: str
    empresa: str
    ano: int
    trimestre: int
    nome_arquivo: str
    caminho_local: str
    url_origem: str
    data_ingestao: str
    status_processamento: str

    @classmethod
    def from_row(cls, row: Any) -> "Documento":
        """Cria uma instância de Documento a partir de uma linha do banco de dados."""
        return cls(
            hash=row["hash"],
            empresa=row["empresa"],
            ano=row["ano"],
            trimestre=row["trimestre"],
            nome_arquivo=row["nome_arquivo"],
            caminho_local=row["caminho_local"],
            url_origem=row["url_origem"],
            data_ingestao=row["data_ingestao"],
            status_processamento=row["status_processamento"]
        )
    
