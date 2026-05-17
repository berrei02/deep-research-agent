from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class ResearchSource(TypedDict):
    url: str
    title: str
    content: str
    relevance_score: float


class ResearchState(TypedDict):
    topic: str
    research_plan: list[str]           # Sub-questions to investigate
    sources: Annotated[list[ResearchSource], lambda a, b: a + b]  # Accumulated sources
    summaries: Annotated[list[str], lambda a, b: a + b]           # Per-round summaries
    iteration: int
    final_report: str
    messages: Annotated[list, add_messages]
