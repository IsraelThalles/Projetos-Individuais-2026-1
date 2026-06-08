from pathlib import Path

DIRETORIO_BASE = Path(__file__).resolve().parent.parent.parent
BANCO_DE_DADOS = DIRETORIO_BASE / "banco" / "banco.db"
DDL = DIRETORIO_BASE / "banco" / "ddl.sql"
PASTA_DADOS = DIRETORIO_BASE / "dados"
ARQUIVO_FONTES = DIRETORIO_BASE / "fonte_de_dados.json"
ARQUIVO_PROMPT_SISTEMA = DIRETORIO_BASE / "prompts" / "prompt_sistema.md"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

GET = "GET"
POST = "POST"