import json
import requests
from pathlib import Path
from constantes import ARQUIVO_FONTES, PASTA_DADOS



def escrever_arquivo(destino: Path, conteudo: requests.Response) -> None:
    """Escreve o conteúdo em um arquivo no destino especificado."""
    with open(destino, "wb") as arquivo:
        for bloco in conteudo.iter_content(1024 * 1024):
            arquivo.write(bloco)



def carregar_arquivo_de_fontes() -> list:
    """Carrega a lista de empresas e seus links a partir do arquivo JSON."""
    with open(
        ARQUIVO_FONTES,
        "r",
        encoding="utf-8"
    ) as arquivo:
        return json.load(arquivo)
    


def extrair_ano_do_nome_do_arquivo(nome_arquivo: str) -> int:
    """Extrai o ano do nome do arquivo, assumindo o formato '[0-4]T[0-9][0-9].pdf'."""
    try:
        return int("20" + nome_arquivo[2:4])
    except (IndexError, ValueError):
        raise ValueError(f"Nome de arquivo inválido para extração de ano: {nome_arquivo}")



def extrair_trimestre_do_nome_do_arquivo(nome_arquivo: str) -> int:
    """Extrai o trimestre do nome do arquivo, assumindo o formato '[0-4]T[0-9][0-9].pdf'."""
    try:
        return int(nome_arquivo[0])
    except (IndexError, ValueError):
        raise ValueError(f"Nome de arquivo inválido para extração de trimestre: {nome_arquivo}")



def criar_arquivo(pasta_da_empresa: Path, previa: dict) -> Path:
    """Cria o caminho do arquivo para a prévia operacional, gerando um nome baseado no ano e trimestre."""
    nome_do_arquivo = gerar_nome_do_arquivo(previa)
    destino = (pasta_da_empresa / f"{nome_do_arquivo}.pdf")

    return destino



def gerar_nome_do_arquivo(previa: dict) -> str:
    """Gera o nome do arquivo com base no ano e trimestre da prévia."""
    return (f"{previa['file_quarter']}T{str(previa['file_year'])[-2:]}")



def criar_pasta_da_empresa(nome_empresa: str) -> Path:
    """Cria a pasta para a empresa, se ainda não existir, e retorna o caminho."""
    pasta_empresa = (
        PASTA_DADOS / nome_empresa
    )

    pasta_empresa.mkdir(
        parents=True,
        exist_ok=True
    )
    
    return pasta_empresa