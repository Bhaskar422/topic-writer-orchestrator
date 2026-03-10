from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from src.state import AgentState
from src.agents.researcher import researcher_agent
from src.agents.writer import writer_agent

load_dotenv()

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("researcher", researcher_agent)
    graph.add_node("writer", writer_agent)

    graph.add_edge(START, "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", END)

    return graph.compile()

    