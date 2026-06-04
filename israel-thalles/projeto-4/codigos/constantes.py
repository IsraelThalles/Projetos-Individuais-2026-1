from pathlib import Path

PASTA_DADOS = Path("dados")
PASTA_DADOS.mkdir(exist_ok=True)
BANCO_DE_DADOS = "banco/banco.db"
DDL = "banco/ddl.sql"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

GET = "GET"
POST = "POST"