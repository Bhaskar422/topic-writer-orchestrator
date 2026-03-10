from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState

def fact_checker_agent(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    messages = [
        SystemMessage(content=(
            "You are a fact checker. Compare the report against the research findings. "
            "Identify any inaccuracies, unsupported claims, or missing key facts. "
            "Format: 'FACT CHECK SCORE: X/10 - <feedback>'"
        )),
        HumanMessage(content=(
            f"Research findings:\n{state['research']}\n\n"
            f"Report to check:\n{state['report']}"
        ))
    ]

    response = llm.invoke(messages)

    return {"fact_check": response.content}