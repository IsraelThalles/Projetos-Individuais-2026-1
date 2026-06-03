from pathlib import Path
import requests
import json
import re
from datetime import datetime
from typing import Literal
from constantes import PASTA_DADOS, HEADERS, GET, POST



def carregar_fontes() -> list:
    """Carrega a lista de empresas e seus links a partir do arquivo JSON."""
    with open(
        "fonte_de_dados.json",
        "r",
        encoding="utf-8"
    ) as arquivo:
        return json.load(arquivo)



def enviar_requisicao(metodo: Literal["GET", "POST"], url: str, **kwargs) -> requests.Response:
    """Envia uma requisição HTTP usando o método especificado para a URL fornecida, com os parâmetros fornecidos."""
    return requests.request(metodo, url, **kwargs)



def obter_html(url: str) -> str:
    """Faz uma requisição HTTP para obter o conteúdo HTML da página."""
    resposta = enviar_requisicao(GET, url, headers=HEADERS, timeout=60)

    resposta.raise_for_status()

    return resposta.text



def extrair_fm_id(html: str) -> str | None:
    """Extrai o fmId da empresa a partir do conteúdo HTML."""
    match = re.search(
        r"var\s+fmId\s*=\s*['\"]([a-f0-9\-]+)['\"]",
        html
    )

    if not match:
        return None

    return match.group(1)



def obter_documentos_do_ano(fm_id: str, ano: int):
    url = (
        f"https://apicatalog.mziq.com/filemanager/company/"
        f"{fm_id}/filter/categories/year/meta"
    )

    payload = {
        "year": str(ano),
        "categories": [
            "central_de_resultados_release",
            "central_de_resultados_previa",
            "central_de_resultados_itr",
            "central_de_resultados_planilha_interativa",
            "central_de_resultados_audio",
            "central_de_resultados_transcricao"
        ],
        "language": "pt_BR",
        "published": True
    }

    resposta = enviar_requisicao(POST, url, json=payload, headers=HEADERS, timeout=120)

    resposta.raise_for_status()

    dados = resposta.json()

    return (
        dados
        .get("data", {})
        .get("document_metas", [])
    )



def filtrar_previas_operacionais(documentos: list) -> list:
    """Filtra os documentos para obter apenas as prévias operacionais"""
    previas = []

    for documento in documentos:

        nome_interno = (
            documento
            .get("internal_name", "")
            .lower()
            .strip()
        )

        titulo = (
            documento
            .get("file_title", "")
            .lower()
        )

        if (
            nome_interno == "central_de_resultados_previa"
            or "prévia" in titulo
            or "previa" in titulo
        ):
            previas.append(documento)

    return previas



def baixar_arquivo(url: str, destino: Path) -> None:
    """Baixa o arquivo da URL fornecida e salva no destino especificado."""
    resposta = enviar_requisicao(GET, url, stream=True, timeout=(30, 300))

    resposta.raise_for_status()

    with open(destino, "wb") as arquivo:
        for bloco in resposta.iter_content(1024 * 1024):
            arquivo.write(bloco)



def processar_empresa(nome_empresa: str, url: str, ano_inicial: int) -> None:
    print(f"\nProcessando {nome_empresa}")

    try:

        fm_id = extrair_fm_id(obter_html(url))

        if not fm_id:
            print("fmId não encontrado.")
            return

        ano_atual = datetime.now().year

        print(f"Anos: {ano_inicial} até {ano_atual}")

        pasta_da_empresa = criar_pasta_da_empresa(nome_empresa)

        total = 0

        for ano in range(ano_inicial, ano_atual + 1):

            documentos = (obter_documentos_do_ano(fm_id, ano))

            if not documentos:
                continue

            previas = filtrar_previas_operacionais(documentos)

            for previa in previas:

                destino = criar_arquivo(pasta_da_empresa, previa)

                if destino.exists():
                    continue

                print(f"Baixando: {destino.name}...")

                baixar_arquivo(previa["file_url"], destino)

                total += 1

        print(
            f"{total} arquivos novos baixados."
        )

    except Exception as erro:
        print(f"Erro: {erro}")



def criar_arquivo(pasta_da_empresa: Path, previa: dict) -> Path:
    """Cria o caminho do arquivo para a prévia operacional, gerando um nome baseado no ano e trimestre."""
    nome_do_arquivo = gerar_nome_do_arquivo(previa)
    destino = (pasta_da_empresa / f"{nome_do_arquivo}.pdf")

    return destino



def gerar_nome_do_arquivo(previa: dict) -> str:
    """Gera o nome do arquivo com base no ano e trimestre da prévia."""
    return (f"{previa['file_quarter']}T{str(previa['file_year'])[-2:]}")



def criar_pasta_da_empresa(nome_empresa: str) -> Path:
    pasta_empresa = (
        PASTA_DADOS / nome_empresa
    )

    pasta_empresa.mkdir(
        exist_ok=True
    )
    
    return pasta_empresa



def obter_dados_recentes():
    empresas = carregar_fontes()

    for empresa in empresas:

        processar_empresa(
            nome_empresa=empresa["Empresa"],
            url=empresa["Link"],
            ano_inicial=empresa["Ano"]
        )



if __name__ == "__main__":
    obter_dados_recentes()