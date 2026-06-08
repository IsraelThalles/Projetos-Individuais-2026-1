import re
import json
import requests
from pathlib import Path
from utilidades.constantes import ARQUIVO_FONTES, PASTA_DADOS
from excecoes.exceções import ErroDeExtracaoDeDados



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
    """
    Extrai o ano do nome do arquivo.

    Exemplos aceitos:
    - 1T25.pdf
    - MRV_2025_3T.pdf
    - Boletim_Conjuntura_2025_3T.pdf
    """

    match = re.search(r"(20\d{2})", nome_arquivo)

    if match:
        return int(match.group(1))

    match = re.search(r"([1-4])T(\d{2})", nome_arquivo)

    if match:
        return int(f"20{match.group(2)}")

    raise ErroDeExtracaoDeDados(
        nome_arquivo=nome_arquivo,
        tipo_dado="ano"
    )



def extrair_trimestre_do_nome_do_arquivo(nome_arquivo: str) -> int:
    """
    Extrai o trimestre do nome do arquivo.

    Exemplos aceitos:
    - 1T25.pdf
    - MRV_2025_3T.pdf
    - Boletim_Conjuntura_2025_3T.pdf
    """

    match = re.search(r"([1-4])T", nome_arquivo)

    if match:
        return int(match.group(1))

    raise ErroDeExtracaoDeDados(
        nome_arquivo=nome_arquivo,
        tipo_dado="trimestre"
    )



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