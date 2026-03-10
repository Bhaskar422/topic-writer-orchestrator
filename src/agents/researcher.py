from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from src.state import AgentState

RESEARCH_PROMPTS = {
    "TECHNICAL": (
        "You are a technical research assistant. Provide detailed findings with "
        "technical depth, including relevant technologies, methodologies, "
        "benchmarks, and implementation details. Use bullet points."
    ),
    "BUSINESS": (
        "You are a business research analyst. Provide findings focused on "
        "market trends, financial impact, competitive landscape, ROI, "
        "and strategic implications. Use bullet points."
    ),
    "GENERAL": (
        "You are a research assistant. Provide detailed, factual findings "
        "organized as bullet points. Focus on key facts, statistics, "
        "and important details. Be thorough but concise."
    ),
}

def researcher_agent(state: AgentState) -> dict:
    search_tool = TavilySearchResults(max_results=5)
    search_results = search_tool.invoke(state["topic"])

    formatted_results = "\n\n".join(
        f"Source: {r['url']}\n{r['content']}" for r in search_results
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    system_prompt = RESEARCH_PROMPTS.get(state.get("category", "GENERAL"), RESEARCH_PROMPTS["GENERAL"])

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=(
            f"Topic: {state['topic']}\n\n"
            f"Search results:\n{formatted_results}"
        ))
    ]

    response = llm.invoke(messages)

    return {
        "research": response.content,
        "messages": [response],
    }