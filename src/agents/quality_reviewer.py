from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState

def quality_reviewer_agent(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    messages = [
        SystemMessage(content=(
            "You are a quality reviewer. Evaluate the report ONLY for structure, "
            "clarity, grammar, and readability. Provide a score from 1-10 and "
            "brief feedback. Format: 'QUALITY SCORE: X/10 - <feedback>'"
        )),
        HumanMessage(content=f"Report to review:\n{state['report']}")
    ]

    response = llm.invoke(messages)

    return {"quality_review": response.content}