# Deep Research Agent

A Deep Research Agent built with [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview), OpenAI, and a containerized PostgreSQL database that serves as both the **agent state store** and a **virtual filesystem** backend.

## Architecture

```
deep-research-agent/
├── pyproject.toml                      # uv project + dependencies
├── .python-version                     # Python 3.11
├── docker-compose.yml                  # PostgreSQL 16 + pgvector container
├── .env.example                        # Environment variables template
├── config.py                           # Central config (loads from .env)
├── agent.py                            # DeepResearchAgent + PostgresBackend
└── notebooks/
    └── research_agent_demo.ipynb       # Interactive demo notebook
```

## PostgreSQL — two roles

| Role | What's stored |
|------|--------------|
| **Agent state** | Checkpoint of the running research graph (enables resumable runs) |
| **Virtual filesystem** | Research artifacts written/read by the agent during a session |

Both are handled by the `PostgresBackend` from `langchain-deepagent[postgres]`. See the [backends docs](https://docs.langchain.com/oss/python/deepagents/backends#use-a-virtual-filesystem) for details.

## Quickstart

### 1. Start PostgreSQL

```bash
docker compose up -d
```

### 2. Install dependencies (uv)

```bash
uv sync
```

### 3. Configure environment

```bash
cp .env.example .env
# Fill in OPENAI_API_KEY (and optionally OPENAI_MODEL)
```

### 4. Open the notebook

```bash
uv run jupyter notebook notebooks/research_agent_demo.ipynb
```

## Usage from Python

```python
import asyncio
from agent import research

result = asyncio.run(research("What are the latest advances in fusion energy?"))
print(result)
```
