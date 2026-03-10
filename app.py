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

st.markdown(
    "Enter a topic below. A **router** classifies it, a **researcher** gathers findings, "
    "a **writer** drafts a report, and a **reviewer** checks quality (with revision loops)."
)

topic = st.text_input("Topic", placeholder="e.g. The impact of AI on healthcare")

if st.button("Generate Report", disabled=not topic):
    graph = build_graph()

    with st.status("Agents working...", expanded=True) as status:
        st.write("Router: classifying topic...")
        result = {"topic": topic, "messages": [], "research": "", "report": "", "category": "", "revision_count": 0}

        steps = []
        for event in graph.stream(result, stream_mode="updates"):
            for node_name, node_output in event.items():
                steps.append(node_name)
                if node_name == "router":
                    st.write(f"Router: classified as **{node_output.get('category', 'N/A')}**")
                elif node_name == "researcher":
                    st.write("Researcher: findings gathered")
                elif node_name == "writer":
                    st.write("Writer: report drafted")
                elif node_name == "reviewer":
                    last_msg = node_output["messages"][-1].content
                    if "APPROVED" in last_msg:
                        st.write("Reviewer: **approved**")
                    else:
                        st.write("Reviewer: revision requested, sending back to writer..")
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

    st.caption(f"Category: {result.get('category', 'N/A')} | Revisions: {result.get('revision_count', 0)}")