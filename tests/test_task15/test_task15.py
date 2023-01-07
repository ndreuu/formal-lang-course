from contextlib import redirect_stdout
from pathlib import Path

import pytest
from pyformlang.cfg import CFG

from project.graph_query_language.interpreter import interpreter
from tests.utils import get_data


@pytest.mark.parametrize(
    "input, expected",
    get_data("test_cfg_intersection_union", lambda d: (d["input"], d["expected"])),
)
def test_cfg_intersection_union(input: str, expected: str, tmp_path: Path):
    input_path = tmp_path / "_.gql"
    out_path = tmp_path / "_.out"

    with open(input_path, "w") as f:
        f.write(input)
    with open(out_path, "w") as f:
        with redirect_stdout(f):
            interpreter([Path(input_path)])
    with open(out_path, "r") as f:
        contents = f.read()

    actual_network = CFG.from_text(contents).to_pda().to_networkx()
    expected_network = CFG.from_text(expected).to_pda().to_networkx()

    assert (
        actual_network.__str__() == expected_network.__str__()
        and actual_network.edges == expected_network.edges
    )


@pytest.mark.parametrize(
    "input, expected",
    get_data("test_scripts", lambda d: (d["input"], d["expected"])),
)
def test_scripts(input: str, expected: str, tmp_path: Path):
    input_path = tmp_path / "_.gql"
    out_path = tmp_path / "_.out"

    with open(input_path, "w") as f:
        f.write(input)
    with open(out_path, "w") as f:
        with redirect_stdout(f):
            interpreter([Path(input_path)])
    with open(out_path, "r") as f:
        contents = f.read()

    assert contents == expected
