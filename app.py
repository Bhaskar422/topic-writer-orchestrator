# from src.graph import build_graph

# def main():
#     graph = build_graph()

#     result = graph.invoke({
#         "topic": "The impact of artificial intelligence on healthcare",
#         "messages": [],
#         "research": "",
#         "report": "",
#         "revision_count": 0,
#     })

#     print("=" * 60)
#     print("RESEARCH FINDINGS")
#     print("=" * 60)
#     print(result["research"])
#     print()
#     print("=" * 60)
#     print("FINAL REPORT")
#     print("=" * 60)
#     print(result["report"])
#     print()
#     print("=" * 60)
#     print(f"REVISIONS: {result['revision_count']}")
#     print("=" * 60)


# if __name__ == "__main__":
#     main()

import streamlit as st
from src.graph import build_graph

st.set_page_config(page_title="Multi-Agent Report Generator", layout="wide")
st.title("Multi-Agent Report Generator")

tab_run, tab_graph = st.tabs(["Run", "Graph"])

with tab_graph:
    st.subheader("Agent Flow")
    graph = build_graph()
    mermaid_str = graph.get_graph().draw_mermaid()
    st.code(mermaid_str, language="text")

with tab_run:
    st.markdown(
        "Enter a topic. A **router** classifies it, a **researcher** gathers findings "
        "(via web search), a **writer** drafts a report, then a **quality reviewer** and "
        "**fact checker** run in parallel before a final reviewer decides."
    )

    topic = st.text_input("Topic", placeholder="e.g. The impact of AI on healthcare")

    if st.button("Generate Report", disabled=not topic):
        graph = build_graph()

        with st.status("Agents working...", expanded=True) as status:
            result = {
                "topic": topic, "messages": [], "research": "", "report": "",
                "category": "", "revision_count": 0, "quality_review": "", "fact_check": "",
            }

            for event in graph.stream(result, stream_mode="updates"):
                for node_name, node_output in event.items():
                    if node_name == "router":
                        st.write(f"Router: classified as **{node_output.get('category', 'N/A')}**")
                    elif node_name == "researcher":
                        st.write("Researcher: findings gathered from web search")
                    elif node_name == "writer":
                        st.write("Writer: report drafted")
                    elif node_name == "quality_reviewer":
                        st.write("Quality Reviewer: evaluation complete (parallel)")
                    elif node_name == "fact_checker":
                        st.write("Fact Checker: verification complete (parallel)")
                    elif node_name == "reviewer":
                        last_msg = node_output["messages"][-1].content
                        if "APPROVED" in last_msg:
                            st.write("Final Reviewer: **approved**")
                        else:
                            st.write("Final Reviewer: revision requested...")
                    elif node_name == "increment_revision":
                        st.write("Starting revision...")

                    result.update(node_output)

            status.update(label="Done!", state="complete")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Research Findings")
            st.markdown(result.get("research", ""))
        with col2:
            st.subheader("Final Report")
            st.markdown(result.get("report", ""))

        with st.expander("Review Details"):
            st.markdown(f"**Quality Review:** {result.get('quality_review', 'N/A')}")
            st.markdown(f"**Fact Check:** {result.get('fact_check', 'N/A')}")

        st.caption(
            f"Category: {result.get('category', 'N/A')} | "
            f"Revisions: {result.get('revision_count', 0)}"
        )