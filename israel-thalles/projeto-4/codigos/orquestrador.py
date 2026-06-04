from utilidades.banco import criar_banco_se_nao_existir, obter_conexao, fechar_conexao
from ingestão import obter_dados_recentes



def main():
    criar_banco_se_nao_existir()
    obter_conexao()
    
    try:
        resultado = obter_dados_recentes()
        if not resultado.sucesso:
            print(f"Erro ao obter dados recentes: {resultado.erro}")
    except Exception as erro:
        print(f"Erro ao obter dados recentes: {erro}")
    finally:
        fechar_conexao()



if __name__ == "__main__":
    main()
