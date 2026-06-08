CREATE TABLE catalogo_documentos (
    hash TEXT PRIMARY KEY,
    publicador TEXT NOT NULL,
    ano INTEGER,
    trimestre INTEGER,
    nome_arquivo TEXT NOT NULL,
    caminho_local TEXT NOT NULL,
    data_ingestao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_processamento TEXT DEFAULT 'PENDENTE'
);

CREATE TABLE metricas_operacionais (
    identificador INTEGER PRIMARY KEY AUTOINCREMENT,
    hash_documento TEXT NOT NULL,
    empresa_referencia TEXT NOT NULL,
    categoria TEXT NOT NULL,
    nome_metrica TEXT NOT NULL,
    valor REAL,
    unidade_medida TEXT,
    FOREIGN KEY (hash_documento) REFERENCES catalogo_documentos(hash) ON DELETE CASCADE
);