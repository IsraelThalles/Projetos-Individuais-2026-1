class ErroDeIdNaoEncontrado(ValueError):
    """fmId não encontrado no HTML da empresa."""
    def __init__(self, empresa: str, url: str):
        super().__init__(f"fmId não encontrado para {empresa} em {url}")
        self.empresa = empresa
        self.url = url



class ErroDeExtracaoDeDados(ValueError):
    """Erro ao extrair dados do nome do arquivo."""
    def __init__(self, nome_arquivo: str, tipo_dado: str):
        super().__init__(f"Não foi possível extrair {tipo_dado} de: {nome_arquivo}")
        self.nome_arquivo = nome_arquivo
        self.tipo_dado = tipo_dado