from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from src.state import AgentState
from src.agents.router import router_agent
from src.agents.researcher import researcher_agent
from src.agents.writer import writer_agent
from src.agents.reviewer import reviewer_agent
from src.agents.quality_reviewer import quality_reviewer_agent
from src.agents.fact_checker import fact_checker_agent

load_dotenv()

MAX_REVISIONS = 2

def should_revise(state:AgentState) -> str:
    """Conditional edge: decides whether to loop back to writer or finish."""
    last_message = state["messages"][-1].content

    if state["revision_count"] >= MAX_REVISIONS:
        return "end"
    
    if "APPROVED" in last_message:
        return "end"
    
    return "revise"

def increment_revision(state: AgentState) -> dict:
    """Small passthrough node that bumps the revision counter."""
    return {"revision_count": state["revision_count"] + 1}

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_agent)
    graph.add_node("researcher", researcher_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("reviewer", reviewer_agent)
    graph.add_node("quality_reviewer", quality_reviewer_agent)
    graph.add_node("fact_checker", fact_checker_agent)
    graph.add_node("increment_revision", increment_revision)

    graph.add_edge(START, "router")
    graph.add_edge("router", "researcher")
    graph.add_edge("researcher", "writer")

    graph.add_edge("writer", "quality_reviewer")
    graph.add_edge("writer", "fact_checker")

    graph.add_edge("quality_reviewer", "reviewer")
    graph.add_edge("fact_checker", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        should_revise,
        {
            "revise": "increment_revision",
            "end": END,
        }
    )

    graph.add_edge("increment_revision", "writer")

    return graph.compile()


def visualize_graph():
    graph = build_graph()
    print(graph.get_graph().draw_mermaid())
