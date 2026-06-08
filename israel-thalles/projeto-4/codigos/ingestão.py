from pathlib import Path
from datetime import datetime
from utilidades.constantes import HEADERS, POST
from utilidades.hash import calcular_hash
from utilidades.banco import buscar_documento_por_hash, salvar_documento
from utilidades.tipos import Documento
from excecoes.exceções import ErroDeIdNaoEncontrado
from utilidades.rede import enviar_requisicao, obter_html, extrair_fm_id, baixar_arquivo
from utilidades.manipular_arquivo import carregar_arquivo_de_fontes, extrair_ano_do_nome_do_arquivo, extrair_trimestre_do_nome_do_arquivo, criar_arquivo, criar_pasta_da_empresa



def obter_documentos_do_ano(fm_id: str, ano: int) -> list:
    """Obtém a lista de documentos para um ano específico usando o fmId da empresa."""
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



def processar_empresa(nome_empresa: str, url: str, ano_inicial: int) -> bool:
    """Processa os dados de uma empresa, baixando as prévias operacionais dos anos especificados."""
    print(f"\nProcessando {nome_empresa}")

    try:

        fm_id = extrair_fm_id(obter_html(url))

        if not fm_id:
            raise ErroDeIdNaoEncontrado(nome_empresa, url)

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

                if not destino.exists():
                    print(f"Baixando: {destino.name}...")

                    try:
                        baixar_arquivo(previa["file_url"], destino)
                    except Exception as erro:
                        print(f"Erro ao baixar {destino.name}: {erro}")
                        continue
                    total += 1             

        print(
            f"{total} arquivos novos baixados."
        )
    except ErroDeIdNaoEncontrado as erro:
        print(f"Erro: {erro}")
    except Exception:
        raise

    return True



def obter_dados_recentes() -> bool:
    """Obtém os dados mais recentes para todas as empresas listadas no arquivo de fontes."""
    empresas = carregar_arquivo_de_fontes()

    try:
        for empresa in empresas:

            processar_empresa(
                nome_empresa=empresa["Empresa"],
                url=empresa["Link"],
                ano_inicial=empresa["Ano"]
            )

    except ValueError as erro:
        print(f"Erro: {erro}")
    except Exception:
        raise

    return True
    



if __name__ == "__main__":
    obter_dados_recentes()