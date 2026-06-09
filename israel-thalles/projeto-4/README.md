# Projeto 4 — Extração de Conjuntura Habitacional

> **Aluno(a):** Israel Thalles Dutra dos Santos
> **Matrícula:** 190014776
> **Data de entrega:** 08/06/2026

---

## Visão Geral

Este projeto automatiza a captura e o processamento de relatórios de prévia operacional do setor imobiliário.
Ele faz o download de documentos financeiros publicados por construtoras, extrai o texto relevante dos PDFs, envia o conteúdo a um modelo de linguagem para gerar métricas estruturadas e salva os resultados em um banco de dados local.

O objetivo é transformar informações não estruturadas de relatórios em métricas operacionais pesquisáveis e acessíveis via API.

## Funcionalidades Principais

- Coleta automática de documentos a partir de URLs de RI (`fonte_de_dados.json`)
- Filtro e download de prévias operacionais por ano
- Extração de texto relevante de PDFs usando `PyMuPDF`
- Inferência estruturada com um modelo de LLM (Google Gemini via `instructor`)
- Persistência de documentos e métricas em SQLite
- API REST para consulta de métricas extraídas

## Estrutura do Projeto

```
projeto-4/
├── banco/
│   ├── ddl.sql
├── codigos/
│   ├── api.py
│   ├── auditar.py
│   ├── contrato_semântico.py
│   ├── estruturar_dados.py
│   ├── extração.py
│   ├── ingestão.py
│   ├── orquestrador.py
│   └── utilidades/
├── dados/
├── prompts/
│   └── prompt_sistema.md
├── fonte_de_dados.json
├── dependências.txt
├── relatorio-entrega.md
└── README.md
```

## Componentes Principais

- `codigos/ingestão.py`: baixa os relatórios das empresas listadas em `fonte_de_dados.json`
- `codigos/auditar.py`: identifica documentos novos ou pendentes antes de processar
- `codigos/extração.py`: filtra páginas relevantes do PDF e extrai o texto
- `codigos/estruturar_dados.py`: envia o texto ao LLM e recebe um relatório estruturado
- `codigos/orquestrador.py`: coordena todo o pipeline de ingestão, extração e persistência
- `codigos/api.py`: expõe uma API FastAPI para consultas de métricas extraídas
- `codigos/utilidades/`: utilitários de banco, rede, manipulação de arquivos, hashing e constantes
- `banco/ddl.sql`: define o esquema SQLite com tabelas de documentos e métricas

## Requisitos

- Python 3.11+ compatível
- Pacotes listados em `dependências.txt`
- Chave de API Google Gemini configurada em `.env`

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r dependências.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com a chave de API:

```env
CHAVE_API=seu_token_aqui
```

## Execução do Pipeline

1. Baixe e processe os relatórios:

```bash
python3 codigos/orquestrador.py
```
> Ou agende a execução na ferramenta de sua preferência. Exemplo: Cron, Systemd Timer, Anacron.

2. O orquestrador realizará as etapas:
- download dos PDFs
- auditoria de arquivos novos/pedentes
- extração de páginas relevantes
- inferência estruturada via LLM
- salvamento das métricas no banco SQLite

## Executando a API

Inicie a API local com:

```bash
cd codigos
uvicorn codigos.api:app --reload --port 8000
```

Acesse a documentação automática em:

```text
http://127.0.0.1:8000/docs
```

## Exemplos de Uso da API

- Buscar todas as métricas:

```bash
curl http://127.0.0.1:8000/api/conjuntura
```

- Filtrar por empresa e ano:

```bash
curl "http://127.0.0.1:8000/api/conjuntura?empresa=MRV&ano=2025"
```

## Observações

- `dados/` armazena os arquivos PDF baixados por empresa
- `fonte_de_dados.json` define os links das empresas e o ano inicial para coleta
- `prompts/prompt_sistema.md` contém o prompt usado para estruturar a saída do modelo
- A tabela `metricas_operacionais` depende da tabela `catalogo_documentos`

## Sobre a Extração de Dados

O projeto prioriza a leitura de páginas que contêm termos-chave do setor imobiliário, como:

- lançamentos
- vendas
- produção
- banco de terrenos
- landbank

Caso nenhuma página relevante seja encontrada, o pipeline usa fallback para extrair o texto completo do PDF.


