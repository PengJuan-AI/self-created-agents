# RAG Researcher

RAG Researcher is an independent document-question-answering agent. It loads a document, builds a retrieval index, and answers questions using retrieved context.

## Current status

This is a private building-stage agent. The current proof of concept is kept in `rag_agent.py`; it still needs configurable document paths, a stable adapter, and a web/API entrypoint before it is promoted in the Hub.

## Run

```bash
python3 rag_agent.py
```

Configure credentials in a local `.env` file. Do not commit source documents, vector stores, or API keys.

## Independence rule

RAG Researcher owns its implementation, dependencies, documentation, and future tests inside this folder. The Hub should call its public adapter rather than importing its internal LangChain graph directly.
