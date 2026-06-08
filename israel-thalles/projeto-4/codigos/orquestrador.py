import time
from ingestão import obter_dados_recentes
from auditar import auditar_documento
from utilidades.constantes import PASTA_DADOS
from utilidades.hash import calcular_hash
from extração import extrair_contexto_relevante
from estruturar_dados import extrair_dados_estruturados
from utilidades.banco import (
    criar_banco_se_nao_existir, 
    obter_conexao, 
    fechar_conexao, 
    salvar_metricas_documento,
    atualizar_status_documento
)



def main():
    criar_banco_se_nao_existir()
    obter_conexao()
    
    try:
        # 1. Faz o download dos PDFs novos das construtoras
        obter_dados_recentes()

        # 2. Varre a pasta procurando arquivos
        for pdf in PASTA_DADOS.rglob("*.pdf"):
            try:
                documento_novo_ou_pendente = auditar_documento(pdf)
                
                if documento_novo_ou_pendente:
                    print(f"\n⚙️ [Orquestrador] Iniciando processamento de: {pdf.name}")
                    
                    texto = extrair_contexto_relevante(pdf)
                    
                    if texto:
                        resultado_ia = extrair_dados_estruturados(texto, pdf.name)
                        hash_doc = calcular_hash(pdf) # Precisamos do hash para atualizar o status
                        
                        if resultado_ia and resultado_ia.metricas:
                            salvar_metricas_documento(hash_doc, resultado_ia.metricas)
                            
                            # --- MÁGICA DO ESTADO: Carimba o sucesso! ---
                            atualizar_status_documento(hash_doc, "CONCLUÍDO")
                            print(f"✅ [Orquestrador] Fluxo concluído e validado para {pdf.name}!")
                        else:
                            print(f"⚠️ Nenhuma métrica encontrada em {pdf.name}.")
                            # Marca como concluído mesmo sem métricas para não ficar em loop eterno
                            atualizar_status_documento(hash_doc, "CONCLUÍDO")
                            
                        print("⏳ Aguardando 15 segundos para evitar bloqueio da API (Erro 503)...")
                        time.sleep(15) 
                            
            except Exception as erro:
                print(f"❌ Erro ao processar o pipeline para {pdf.name}: {erro}")
                # --- MÁGICA DO ESTADO: Carimba a falha! ---
                hash_doc_erro = calcular_hash(pdf)
                atualizar_status_documento(hash_doc_erro, "ERRO")
                
    except Exception as erro:
        print(f"Erro ao obter dados recentes: {erro}")
    finally:
        fechar_conexao()



if __name__ == "__main__":
    main()
