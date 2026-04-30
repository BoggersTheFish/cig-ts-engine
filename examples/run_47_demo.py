from pathlib import Path

from cig.engine import ThinkingSystemEngine
from cig.io import load_graph_yaml


def main() -> None:
    graph = load_graph_yaml(Path(__file__).with_name("ts_core.yaml"))
    engine = ThinkingSystemEngine(graph)
    engine.step()
    print(graph.node("prime"))


if __name__ == "__main__":
    main()

