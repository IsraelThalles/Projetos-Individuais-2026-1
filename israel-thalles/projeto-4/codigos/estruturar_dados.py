import os
import instructor
from typing import cast
from google import genai
from openai import OpenAI
from utilidades.manipular_arquivo import ler_prompt_sistema
from contrato_semântico import RelatorioConjuntura
from dotenv import load_dotenv



load_dotenv()



def extrair_dados_estruturados(texto_contexto: str, nome_arquivo_pdf: str) -> RelatorioConjuntura:
    """
    Envia o texto do PDF para o LLM e retorna no formato da classe RelatorioConjuntura.
    """
    cliente_local = genai.Client(
        api_key=os.getenv("CHAVE_API")
    )

    cliente = instructor.from_genai(
        cliente_local, 
        mode=instructor.Mode.GENAI_STRUCTURED_OUTPUTS
    )

    print(f"  [🧠] Iniciando inferência para: {nome_arquivo_pdf}...")

    prompt_sistema = ler_prompt_sistema()

    try:
        dados_estruturados = cliente.chat.completions.create(
            model="gemini-2.5-flash",
            response_model=RelatorioConjuntura,
            
            config={
                "temperature": 0.0,
                "max_output_tokens": 8192 
            },
            max_retries=2,
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


