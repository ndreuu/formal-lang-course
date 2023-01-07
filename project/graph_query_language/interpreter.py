import sys
from pathlib import Path

from project.graph_query_language.gql_exceptions import (
    RunTimeException,
    InvalidScriptPath,
    InvalidScriptExtension,
)
from project.graph_query_language.parser import parse
from project.graph_query_language.visitor import Visitor


def __interpreter(input_text: str):
    parser = parse(text=input_text)
    tree = parser.prog()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise RunTimeException("Invalid syntax of program")

    visitor = Visitor()
    visitor.visit(tree)

    return 0


def interp(txt):
    return __interpreter(txt)


def interpreter(*argv):
    if len(argv[0]) == 0:
        sys.stdout.write("GQL console mode:\n")
        program = "".join(sys.stdin.readlines())
    else:
        program = read_script(filename=Path(argv[0][0]))

    return __interpreter(program)


def read_script(filename: Path) -> str:
    try:
        script = filename.open()
    except FileNotFoundError as e:
        raise InvalidScriptPath(filename.name) from e

    if not filename.name.endswith(".gql"):
        raise InvalidScriptExtension()

    return "".join(script.readlines())
