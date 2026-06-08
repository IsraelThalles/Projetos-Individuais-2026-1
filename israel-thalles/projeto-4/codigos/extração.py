import fitz
from pathlib import Path



def extrair_contexto_relevante(caminho_pdf: Path) -> str:
    """
    Lê o PDF e extrai apenas o texto das páginas que contêm as palavras-chave operacionais.
    Descarta capas, introduções institucionais e páginas puramente visuais.
    """
    
    PALAVRAS_CHAVE = [
        "lançamento", "lançamentos", 
        "venda", "vendas", "vgv", 
        "produção", "banco de terrenos", "landbank"
    ]
    
    try:
        with fitz.open(caminho_pdf) as documento:
            paginas_relevantes: list[str] = []
            qtd_selecionada = 0
            total_paginas = documento.page_count
            
            for num_pagina in range(total_paginas):
                pagina = documento.load_page(num_pagina)
                texto_pagina = str(pagina.get_text("text"))
                texto_minusculo = texto_pagina.lower()
                
                if any(palavra in texto_minusculo for palavra in PALAVRAS_CHAVE):
                    paginas_relevantes.append(f"--- CONTEÚDO DA PÁGINA {num_pagina + 1} ---\n{texto_pagina}\n")
                    qtd_selecionada += 1
                    
            print(f"  [>] Arquivo {caminho_pdf.name}: {qtd_selecionada}/{total_paginas} páginas filtradas.")
            
            if not paginas_relevantes:
                print(f"  [!] Alerta: Nenhuma palavra-chave encontrada. Enviando todo o PDF: {caminho_pdf.name}")
                return extrair_texto_completo(caminho_pdf)
                
            return "\n".join(paginas_relevantes)
        
    except Exception as e:
        print(f"Erro ao processar o PDF {caminho_pdf.name}: {e}")
        return ""



def extrair_texto_completo(caminho_pdf: Path) -> str:
    """Função de fallback caso o chunking heurístico falhe."""
    try:
        with fitz.open(caminho_pdf) as documento:
            texto_completo: list[str] = []
            
            for num_pagina in range(documento.page_count):
                pagina = documento.load_page(num_pagina)
                texto_completo.append(str(pagina.get_text("text")))
                
            return "\n".join(texto_completo)
            
    except Exception as e:
        print(f"Erro na extração completa do PDF {caminho_pdf.name}: {e}")
        return ""

