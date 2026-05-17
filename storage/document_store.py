from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import config


class ResearchDocumentStore:
    """Persistent vector store for retrieved research documents."""

    def __init__(self, collection: str = "research_docs", db_uri: str = config.DATABASE_URL):
        self._store = PGVector(
            embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
            collection_name=collection,
            connection=db_uri,
            use_jsonb=True,
        )

    def add_sources(self, sources: list[dict], metadata: dict | None = None) -> None:
        docs = [
            Document(
                page_content=s["content"],
                metadata={"url": s["url"], "title": s["title"], **(metadata or {})},
            )
            for s in sources
            if s.get("content")
        ]
        if docs:
            self._store.add_documents(docs)

    def similarity_search(self, query: str, k: int = 5) -> list[Document]:
        return self._store.similarity_search(query, k=k)
