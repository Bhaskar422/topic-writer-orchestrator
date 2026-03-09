from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState


def writer_agent(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    messages = [
        SystemMessage(content = (
            "You are a skilled report writer. Given research findings, write a "
            "well-structured, clear, and engaging report. Use sections with headers, "
            "an introduction, key findings, and a conclusion."
        )),
        HumanMessage(content=(
            f"Write a report on: {state['topic']}\n\n"
            f"Based on these research findings:\n{state['research']}"
        ))
    ]

    response = llm.invoke(messages)

    return {
        "report": response.content,
        "messages": [response],
    }