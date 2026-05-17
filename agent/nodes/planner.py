from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from agent.state import ResearchState
import config
import json

_llm = ChatOpenAI(model=config.OPENAI_MODEL, temperature=0)

SYSTEM_PROMPT = """You are a research planning assistant. Given a research topic,
break it down into 3-5 specific sub-questions that together would produce a comprehensive
understanding of the topic. Return a JSON array of strings, each being a focused sub-question.

Example output:
["What is the history of X?", "What are the main applications of X?", "What are the limitations of X?"]
"""


def plan_research(state: ResearchState) -> dict:
    topic = state["topic"]
    response = _llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Research topic: {topic}"),
    ])

    try:
        plan = json.loads(response.content)
        if not isinstance(plan, list):
            plan = [topic]
    except (json.JSONDecodeError, ValueError):
        plan = [topic]

    return {
        "research_plan": plan,
        "iteration": 0,
        "messages": [HumanMessage(content=f"Researching: {topic}")],
    }
