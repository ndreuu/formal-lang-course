from project.graph_query_language.parser import parse
from project.graph_query_language.types.gql_type import GQLType
from project.graph_query_language.visitor import Visitor


def interpreter_with_value(text: str, token: str) -> GQLType:
    parser = parse(text)
    parser.removeErrorListeners()
    tree = getattr(parser, token)()
    visitor = Visitor()
    return visitor.visit(tree)
