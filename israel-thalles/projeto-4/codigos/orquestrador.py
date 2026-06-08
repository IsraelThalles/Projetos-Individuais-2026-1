from utilidades.banco import criar_banco_se_nao_existir, obter_conexao, fechar_conexao
from ingestão import obter_dados_recentes, auditar_documento
from utilidades.constantes import PASTA_DADOS


def main():
    criar_banco_se_nao_existir()
    obter_conexao()
    
    try:
        obter_dados_recentes()

        for pdf in PASTA_DADOS.rglob("*.pdf"):
            auditar_documento(pdf)
    except Exception as erro:
        print(f"Erro ao obter dados recentes: {erro}")
    finally:
        fechar_conexao()



if __name__ == "__main__":
    main()
