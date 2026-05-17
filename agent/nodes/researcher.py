from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from tavily import TavilyClient
from agent.state import ResearchState, ResearchSource
import config

_llm = ChatOpenAI(model=config.OPENAI_MODEL, temperature=0)


def _search(query: str) -> list[ResearchSource]:
    if not config.TAVILY_API_KEY:
        return [ResearchSource(
            url="https://example.com",
            title="[Tavily API key not set]",
            content=f"No search results available. Configure TAVILY_API_KEY to enable web research for: {query}",
            relevance_score=0.0,
        )]

    client = TavilyClient(api_key=config.TAVILY_API_KEY)
    results = client.search(
        query=query,
        max_results=config.MAX_SEARCH_RESULTS,
        include_raw_content=True,
    )
    return [
        ResearchSource(
            url=r.get("url", ""),
            title=r.get("title", ""),
            content=r.get("content", "") or r.get("raw_content", ""),
            relevance_score=r.get("score", 0.0),
        )
        for r in results.get("results", [])
    ]


def execute_research(state: ResearchState) -> dict:
    plan = state["research_plan"]
    iteration = state.get("iteration", 0)

    if iteration >= len(plan):
        return {"iteration": iteration}

    query = plan[iteration]
    sources = _search(query)

    source_texts = "\n\n".join(
        f"**{s['title']}** ({s['url']})\n{s['content'][:800]}"
        for s in sources
    )

    summary_response = _llm.invoke(
        f"Summarize the following sources in 2-3 paragraphs for the research question: '{query}'\n\n{source_texts}"
    )
    summary = f"### {query}\n{summary_response.content}"

    return {
        "sources": sources,
        "summaries": [summary],
        "iteration": iteration + 1,
        "messages": [AIMessage(content=f"Completed research round {iteration + 1}: {query}")],
    }
