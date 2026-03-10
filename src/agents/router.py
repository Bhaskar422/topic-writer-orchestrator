from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.state import AgentState

def router_agent(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content=(
            "You are a query classifier. Given a user's topic, classify it into "
            "EXACTLY one of these categories:\n"
            "- TECHNICAL: technology, programming, engineering, science\n"
            "- BUSINESS: finance, economics, markets, strategy\n"
            "- GENERAL: everything else\n\n"
            "Respond with ONLY the category name, nothing else."
        )),
        HumanMessage(content=state["topic"])
    ]

    response = llm.invoke(messages)
    category = response.content.strip().upper()

    if category not in ("TECHNICAL", "BUSINESS", "GENERAL"):
        category = "GENERAL"
    
    return {
        "category": category,
        "messages": [response],
    }