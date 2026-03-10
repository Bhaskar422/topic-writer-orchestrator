from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.state import AgentState


def reviewer_agent(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    messages = [
        SystemMessage(content=(
            "You are a strict report reviewer. Evaluate the report for clarity, "
            "accuracy, structure, and completeness. "
            "Respond with EXACTLY one of these formats:\n"
            "- If the report is good: 'APPROVED: <brief praise>'\n"
            "- If it needs work: 'REVISION NEEDED: <specific feedback on what to improve>'"
        )),
        HumanMessage(content=(
            f"Topic: {state['topic']}\n\n"
            f"Research findings:\n{state['research']}\n\n"
            f"Report to review:\n{state['report']}"
        ))
    ]

    response = llm.invoke(messages)

    return {
        "messages": [response]
    }