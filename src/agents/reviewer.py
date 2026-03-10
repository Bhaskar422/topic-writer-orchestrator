from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.state import AgentState


def reviewer_agent(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    messages = [
        SystemMessage(content=(
            "You are the final reviewer. You have received a quality review and a "
            "fact check of a report. Based on BOTH reviews, make a final decision.\n"
            "Respond with EXACTLY one of these formats:\n"
            "- If the report is good: 'APPROVED: <brief summary>'\n"
            "- If it needs work: 'REVISION NEEDED: <specific feedback combining both reviews>'"
        )),
        HumanMessage(content=(
            f"Quality review:\n{state.get('quality_review', 'N/A')}\n\n"
            f"Fact check:\n{state.get('fact_check', 'N/A')}\n\n"
            f"Report:\n{state['report']}"
        ))
    ]

    response = llm.invoke(messages)

    return {
        "messages": [response]
    }