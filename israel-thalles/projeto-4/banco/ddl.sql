CREATE TABLE catalogo_documentos (
    hash TEXT PRIMARY KEY,
    empresa TEXT NOT NULL,
    ano INTEGER,
    trimestre TEXT,
    nome_arquivo TEXT NOT NULL,
    caminho_local TEXT NOT NULL,
    url_origem TEXT NOT NULL,
    data_ingestao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_processamento TEXT DEFAULT 'PENDENTE'
);