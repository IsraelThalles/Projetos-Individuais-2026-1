from pathlib import Path
from datetime import datetime
from utilidades.banco import buscar_documento_por_hash, salvar_documento
from utilidades.tipos import Documento
from excecoes.exceções import ErroDeExtracaoDeDados
from utilidades.manipular_arquivo import extrair_ano_do_nome_do_arquivo, extrair_trimestre_do_nome_do_arquivo
from utilidades.hash import calcular_hash



def auditar_documento(caminho_arquivo: Path) -> bool:
    """Audita um documento verificando se ele já existe no banco de dados pelo seu hash e foi processado. Se for um documento novo, salva suas informações no banco de dados."""
    hash_do_documento = calcular_hash(caminho_arquivo)
    documento_existente = buscar_documento_por_hash(hash_do_documento)

    if documento_existente:
        if documento_existente.status_processamento == "CONCLUÍDO":
            return False
        
        # Se parou no meio (PENDENTE ou ERRO), tenta de novo sem inserir de novo!
        print(f"🔄 Retomando arquivo travado anteriormente: {caminho_arquivo.name}")
        return True
    
    try:
        documento = Documento(
            hash=hash_do_documento,
            publicador=caminho_arquivo.parent.name,
            ano=extrair_ano_do_nome_do_arquivo(caminho_arquivo.name),
            trimestre=extrair_trimestre_do_nome_do_arquivo(caminho_arquivo.name),
            nome_arquivo=caminho_arquivo.name,
            caminho_local=str(caminho_arquivo),
            data_ingestao=datetime.now().isoformat(),
            status_processamento="PENDENTE"
        )

        print(f"Hash do documento: {documento.hash}")

        salvar_documento(documento)

    except ErroDeExtracaoDeDados as erro:
        print(f"Ignorando {erro.nome_arquivo}: {erro}")
        return False
    except Exception:
        raise

    return True