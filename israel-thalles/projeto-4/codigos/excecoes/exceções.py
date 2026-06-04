class ErroDeIdNaoEncontrado(ValueError):
    """fmId não encontrado no HTML da empresa."""
    def __init__(self, empresa: str, url: str):
        super().__init__(f"fmId não encontrado para {empresa} em {url}")
        self.empresa = empresa
        self.url = url