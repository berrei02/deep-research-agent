from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from agent.state import ResearchState
from agent.nodes import plan_research, execute_research, synthesize_report
import config


def _should_continue(state: ResearchState) -> str:
    """Loop researcher until all sub-questions are covered or max iterations hit."""
    iteration = state.get("iteration", 0)
    plan = state.get("research_plan", [])
    if iteration >= len(plan) or iteration >= config.MAX_RESEARCH_ITERATIONS:
        return "synthesize"
    return "research"


def build_graph(checkpointer=None) -> StateGraph:
    graph = StateGraph(ResearchState)

    graph.add_node("planner", plan_research)
    graph.add_node("researcher", execute_research)
    graph.add_node("synthesizer", synthesize_report)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_conditional_edges(
        "researcher",
        _should_continue,
        {"research": "researcher", "synthesize": "synthesizer"},
    )
    graph.add_edge("synthesizer", END)

    return graph.compile(checkpointer=checkpointer)


def run_research(topic: str, thread_id: str, db_uri: str = config.DATABASE_URL) -> dict:
    """Run research with PostgreSQL-backed state persistence."""
    with PostgresSaver.from_conn_string(db_uri) as saver:
        saver.setup()
        app = build_graph(checkpointer=saver)
        config_dict = {"configurable": {"thread_id": thread_id}}
        result = app.invoke({"topic": topic, "sources": [], "summaries": [], "messages": []}, config_dict)
    return result
