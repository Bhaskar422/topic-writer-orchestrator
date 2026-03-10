from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    topic: str
    category: str
    research: str
    report: str
    revision_count: int
    quality_review: str
    fact_check: str