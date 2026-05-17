from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from agent.state import ResearchState
import config

_llm = ChatOpenAI(model=config.OPENAI_MODEL, temperature=0.2)

SYSTEM_PROMPT = """You are a research report writer. Given a topic and a set of research summaries,
produce a comprehensive, well-structured report with:
1. An executive summary
2. Key findings (organized by sub-topic)
3. Conclusion

Cite sources inline using [Source Title] notation. Be thorough but concise.
"""


def synthesize_report(state: ResearchState) -> dict:
    topic = state["topic"]
    summaries = "\n\n".join(state.get("summaries", []))
    sources = state.get("sources", [])

    source_list = "\n".join(f"- {s['title']}: {s['url']}" for s in sources if s.get("url"))

    prompt = (
        f"Topic: {topic}\n\n"
        f"Research Findings:\n{summaries}\n\n"
        f"Sources:\n{source_list}"
    )

    response = _llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])

    return {
        "final_report": response.content,
        "messages": [AIMessage(content="Research complete. Final report generated.")],
    }
