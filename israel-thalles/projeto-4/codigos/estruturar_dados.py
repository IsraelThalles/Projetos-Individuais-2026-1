import os
import instructor
from typing import cast
from openai import OpenAI
from utilidades.manipular_arquivo import ler_prompt_sistema
from contrato_semântico import RelatorioConjuntura
from dotenv import load_dotenv



load_dotenv()



def extrair_dados_estruturados(texto_contexto: str, nome_arquivo_pdf: str) -> RelatorioConjuntura:
    """
    Envia o texto do PDF para o LLM e retorna no formato da classe RelatorioConjuntura.
    """
    cliente_local = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    cliente = instructor.from_openai(
        cliente_local,
        mode=instructor.Mode.JSON
    )

    print(f"  [🧠] Iniciando inferência para: {nome_arquivo_pdf}...")

    prompt_sistema = ler_prompt_sistema()

    try:
        dados_estruturados = cliente.chat.completions.create(
            model="gemma4:e2b",
            response_model=RelatorioConjuntura,
            
            temperature=0.0, 
            
            max_retries=0,
            messages=[
                {
                    "role": "system",
                    "content": prompt_sistema
                },
                {
                    "role": "user",
                    "content": f"Arquivo origem: {nome_arquivo_pdf}\n\nTexto do documento:\n{texto_contexto}"
                }
            ]
        )
        return cast(RelatorioConjuntura, dados_estruturados)
        
    except Exception as e:
        print(f"Erro na extração do LLM local: {e}")
        raise e


