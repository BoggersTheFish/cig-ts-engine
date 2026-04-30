from pathlib import Path

from cig.io import load_graph_yaml
from cig.meaning import meaning_derivative


def main() -> None:
    graph = load_graph_yaml(Path(__file__).with_name("ts_core.yaml"))
    derivative = meaning_derivative(graph, input_node_id="religion")
    print(derivative)


if __name__ == "__main__":
    main()

