from src.graph import build_graph

def main():
    graph = build_graph()

    result = graph.invoke({
        "topic": "The impact of artificial intelligence on healthcare",
        "messages": [],
        "research": "",
        "report": "",
    })

    print("=" * 60)
    print("RESEARCH FINDINGS")
    print("=" * 60)
    print(result["research"])
    print()
    print("=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(result["report"])


if __name__ == "__main__":
    main()