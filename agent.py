"""
Deep Research Agent using langchain-deepagent with PostgreSQL virtual filesystem backend.

Docs:
  Overview : https://docs.langchain.com/oss/python/deepagents/overview
  Backends : https://docs.langchain.com/oss/python/deepagents/backends
"""

from langchain_deepagent import DeepResearchAgent
from langchain_deepagent.backends import PostgresBackend
from langchain_openai import ChatOpenAI

from config import DATABASE_URL, OPENAI_API_KEY, OPENAI_MODEL


def create_agent() -> DeepResearchAgent:
    """Return a DeepResearchAgent backed by PostgreSQL (state + virtual filesystem)."""
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
    )

    # PostgreSQL acts as both the agent state store and the virtual filesystem.
    # The backend persists all intermediate research artifacts to the DB so that
    # long-running or interrupted runs can be resumed.
    backend = PostgresBackend(connection_string=DATABASE_URL)

    return DeepResearchAgent(llm=llm, backend=backend)


async def research(query: str) -> str:
    """Run a deep research query and return the final report."""
    agent = create_agent()
    result = await agent.ainvoke(query)
    return result
