from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cig.report import generate_proof_report


def main() -> None:
    output_path = generate_proof_report(
        output_path=PROJECT_ROOT / "docs/proof_bank/TS-012-prebuilt-concept-graph.md",
        graph_path=PROJECT_ROOT / "examples/ts_core.yaml",
    )
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
