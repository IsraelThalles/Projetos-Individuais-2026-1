import re
import requests
from pathlib import Path
from typing import Literal
from constantes import HEADERS, GET
from manipular_arquivo import escrever_arquivo



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



def baixar_arquivo(url: str, destino: Path) -> None:
    """Baixa o arquivo da URL fornecida e salva no destino especificado."""
    resposta = enviar_requisicao(GET, url, stream=True, timeout=(30, 300))

    resposta.raise_for_status()

    escrever_arquivo(destino, resposta)


