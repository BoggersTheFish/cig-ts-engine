from typer.testing import CliRunner

from cig.cli import app


runner = CliRunner()
GRAPH_PATH = "examples/ts_core.yaml"


def test_cli_run_command() -> None:
    result = runner.invoke(
        app,
        [
            "run",
            GRAPH_PATH,
            "--input",
            "meaning",
            "--input",
            "life",
            "--input",
            "number_47",
            "--steps",
            "6",
        ],
    )

    assert result.exit_code == 0
    assert "top activations:" in result.stdout
    assert "tension before:" in result.stdout
    assert "tension after:" in result.stdout


def test_cli_tension_command() -> None:
    result = runner.invoke(app, ["tension", GRAPH_PATH])

    assert result.exit_code == 0
    assert "total tension:" in result.stdout
    assert "top tension edges:" in result.stdout


def test_cli_derivative_command() -> None:
    result = runner.invoke(
        app,
        [
            "derivative",
            GRAPH_PATH,
            "--input",
            "religion",
            "--context",
            "comfort",
            "--steps",
            "6",
        ],
    )

    assert result.exit_code == 0
    assert "top derivative nodes:" in result.stdout
    assert "ritual" in result.stdout


def test_cli_evolve_command() -> None:
    result = runner.invoke(app, ["evolve", GRAPH_PATH, "--node", "religion"])

    assert result.exit_code == 0
    assert "overloaded node report:" in result.stdout
    assert "context split suggestion:" in result.stdout
    assert "religion_comfort" in result.stdout
    assert "religion_harm" in result.stdout
