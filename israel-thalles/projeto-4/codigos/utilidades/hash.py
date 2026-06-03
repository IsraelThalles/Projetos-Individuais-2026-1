import hashlib
from pathlib import Path



def calcular_hash(caminho_arquivo: Path) -> str:
    """Calcula o hash SHA-256 do arquivo especificado."""
    sha256 = hashlib.sha256()

    with open(caminho_arquivo, "rb") as arquivo:
        for bloco in iter(
            lambda: arquivo.read(1024 * 1024),
            b""
        ):
            sha256.update(bloco)

    return sha256.hexdigest()