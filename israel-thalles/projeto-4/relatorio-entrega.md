# Relatório de Entrega — Projeto Individual 4

> **Aluno(a):** Israel Thalles Dutra dos Santos
> **Matrícula:** 190014776
> **Data de entrega:** 08/06/2026

---

## 1. Resumo do Projeto

O projeto automatiza a extração de métricas operacionais e financeiras de relatórios de prévia operacional do setor imobiliário.
Ele coleta PDFs de relatórios publicados por construtoras, processa o texto relevante com heurísticas e utiliza um LLM para converter o conteúdo em dados estruturados.
Os resultados são salvos em um banco SQLite e disponibilizados por meio de uma API REST.

---

## 2. Objetivos

- Automatizar a ingestão de relatórios financeiros publicados por empresas do setor.
- Extrair texto relevante de PDFs focando em métricas como lançamentos, vendas, produção e banco de terrenos.
- Utilizar LLM para estruturar a informação em métricas padronizadas.
- Persistir documentos e métricas em banco de dados local.
- Expor os resultados via API para consultas filtradas.

---

## 3. Abordagem

O pipeline do projeto é composto por três etapas principais:

1. **Ingestão de Dados**
   - `codigos/ingestão.py` lê `fonte_de_dados.json` com empresas, URLs e anos iniciais.
   - Para cada empresa, recupera o `fmId` e baixa documentos de prévia operacional.
   - Os arquivos são armazenados em `dados/` separados por empresa.

2. **Extração e Inferência**
   - `codigos/extração.py` procura páginas de PDF que mencionam termos-chave do setor.
   - O texto relevante é enviado ao LLM via `codigos/estruturar_dados.py`.
   - A resposta é convertida para o formato `RelatorioConjuntura` definido em `codigos/contrato_semântico.py`.

3. **Persistência e API**
   - `codigos/utilidades/banco.py` mantém o catálogo de documentos e as métricas extraídas.
   - `codigos/api.py` expõe `/api/conjuntura` para consulta com filtros por empresa, ano, trimestre e categoria.

---

## 4. Arquitetura do Pipeline

```
fonte_de_dados.json -> ingestão -> dados/ (PDFs)
                                      ↓
                                 auditoria
                                      ↓
                                   extração
                                      ↓
                          inferência LLM (Google Gemini)
                                      ↓
                           armazenamento SQLite / API
                           FastAPI
```

---

## 5. Como Executar

### 5.1 Instalar dependências

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r dependências.txt
```

### 5.2 Configurar a chave de API

Crie o arquivo `.env` na raiz do projeto:

```env
CHAVE_API=seu_token_aqui
```

### 5.3 Executar o pipeline

```bash
python3 codigos/orquestrador.py
```

### 5.4 Iniciar a API

```bash
cd codigos
uvicorn api:app --reload --port 8000
```

### 5.5 Consultar a API

- Documentação interativa: `http://127.0.0.1:8000/docs`
- Exemplo de endpoint:
  - `http://127.0.0.1:8000/api/conjuntura?empresa=MRV&ano=2025`

---

## 6. Entregáveis

- `codigos/`: código do pipeline, extração, inferência e API.
- `fonte_de_dados.json`: lista de empresas e anos de ingestão.
- `prompts/prompt_sistema.md`: prompt principal para LLM.
- `banco/ddl.sql`: esquema de banco de dados.
- `dependências.txt`: dependências do projeto.
- `README.md`: documentação do projeto.
- `relatorio-entrega.md`: relato e entrega formal.

---

## 7. Observações Finais

- A extração prioriza palavras-chave do setor imobiliário e utiliza fallback para o texto completo quando necessário.
- A base de dados registra estados de processamento: `PENDENTE`, `CONCLUÍDO` e `ERRO`.
- A API retorna uma lista de métricas prontas para análise ou visualização.

