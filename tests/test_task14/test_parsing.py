import pytest
from pathlib import Path

from project.graph_query_language.parser import check_parser_correct, generate_dot
from tests.utils import get_data


@pytest.mark.parametrize(
    "input, is_correct",
    get_data("test_check_parser_correct", lambda d: (d["input"], d["is_correct"])),
)
def test_check_parser_correct(input: str, is_correct: bool):
    print(check_parser_correct(input))
    assert check_parser_correct(input) == is_correct


@pytest.mark.parametrize(
    "input, expected",
    get_data("test_generate_dot", lambda d: (d["input"], d["expected"])),
)
def test_save_parse_tree_as_dot(input: str, expected: str, tmp_path: Path):
    path = tmp_path / "_.dot"
    generate_dot(input, path)
    with open(path, "r") as f:
        contents = f.read()
        assert contents == expected
