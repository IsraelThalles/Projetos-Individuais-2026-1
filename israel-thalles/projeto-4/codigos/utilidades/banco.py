import sqlite3
from pathlib import Path
from typing import Optional
from utilidades.constantes import BANCO_DE_DADOS, DDL
from utilidades.tipos import Documento
from contrato_semântico import MetricaOperacional


_conexao: sqlite3.Connection | None = None

def criar_banco_se_nao_existir() -> None:
    """Cria o banco de dados executando o DDL se ele não existir."""

    caminho_ddl = Path(DDL)
    caminho_banco = Path(BANCO_DE_DADOS)

    if not caminho_banco.exists():
        print(f"Banco de dados não encontrado. Criando {str(caminho_banco)}...")

        if not caminho_ddl.exists():
            raise FileNotFoundError(f"Arquivo DDL não encontrado: {str(caminho_ddl)}")

        conn = sqlite3.connect(caminho_banco)
        with open(caminho_ddl, 'r', encoding='utf-8') as arquivo:
            conn.executescript(arquivo.read())
        conn.close()
        print(f"✓ Banco de dados criado com sucesso!")
    else:
        print(f"✓ Banco de dados já existe: {caminho_banco.name}")



def obter_conexao() -> sqlite3.Connection:
    """Obtém uma conexão com o banco de dados."""
    global _conexao

    if not _conexao:
        _conexao = sqlite3.connect(BANCO_DE_DADOS)
        _conexao.row_factory = sqlite3.Row

    return _conexao



def fechar_conexao() -> None:
    """Fecha a conexão com o banco de dados, se estiver aberta."""
    global _conexao

    if _conexao is not None:
        _conexao.close()
        _conexao = None



def executar_consulta(sql: str, parametros: tuple = (), fetchone: bool = False, fetchall: bool = False) -> Optional[sqlite3.Row] | list[sqlite3.Row]:
    """Executa uma consulta SQL e retorna os resultados."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(sql, parametros)

    if fetchone:
        resultados = cursor.fetchone()
    elif fetchall:
        resultados = cursor.fetchall()
    else:
        conn.commit()
        resultados = None

    return resultados



def buscar_documento_por_hash(hash_do_documento: str) -> Optional[Documento]:
    """Busca um documento no banco de dados pelo seu hash."""
    consulta = """
        SELECT
            *
        FROM
            catalogo_documentos
        WHERE hash = ?
    """

    resultado = executar_consulta(consulta, (hash_do_documento,), fetchone=True)

    return Documento.from_row(resultado) if resultado else None



def salvar_documento(documento: Documento) -> bool:
    """Insere um novo documento no banco de dados."""
    consulta = """
        INSERT INTO catalogo_documentos
            (hash, publicador, ano, trimestre, nome_arquivo, caminho_local)
        VALUES
            (?, ?, ?, ?, ?, ?)
    """

    try:
        executar_consulta(consulta, (documento.hash, documento.publicador, documento.ano, documento.trimestre, documento.nome_arquivo, documento.caminho_local))
        print(f"✓ Documento salvo no banco de dados: {documento.nome_arquivo} (Hash: {documento.hash})")
    except sqlite3.Error:
        raise

    return True



def salvar_metricas_documento(hash_documento: str, metricas: list[MetricaOperacional]) -> bool:
    """Insere em lote todas as métricas extraídas de um documento."""
    consulta = """
        INSERT INTO metricas_operacionais 
            (hash_documento, empresa_referencia, categoria, nome_metrica, valor, unidade_medida)
        VALUES 
            (?, ?, ?, ?, ?, ?)
    """
    
    try:
        for metrica in metricas:
            executar_consulta(consulta, (
                hash_documento,
                metrica.empresa_referencia,
                metrica.categoria,
                metrica.nome_metrica,
                metrica.valor,
                metrica.unidade_medida
            ))
        
        print(f"✓ {len(metricas)} métricas operacionais salvas com sucesso!")
    except sqlite3.Error:
        raise
    return True