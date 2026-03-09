from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState

def researcher_agent(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    messages = [
        SystemMessage(content=(
            "You are a research assistant. Given a topic, provide detailed, "
            "factual findings organized as bullet points. Focus on key facts, "
            "statistics, and important details. Be thorough but concise."
        )),
        HumanMessage(content=f"Research the following topic:\n\n{state['topic']}")
    ]

    response = llm.invoke(messages)

    return {
        "research": response.content,
        "messages": [response],
    }