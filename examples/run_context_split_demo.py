from pathlib import Path

from cig.io import load_graph_yaml


def main() -> None:
    graph = load_graph_yaml(Path(__file__).with_name("ts_core.yaml"))
    contexts = graph.split_by_context()
    for context, subgraph in contexts.items():
        print(context, sorted(subgraph.nodes))


if __name__ == "__main__":
    main()

