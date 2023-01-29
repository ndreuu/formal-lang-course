from project.graph_query_language.gql_exceptions import NotImplementedException
from project.graph_query_language.types.gql_type import GQLType


class Bool(GQLType):
    def __init__(self, b: bool):
        self.b = b

    def __bool__(self):
        return self.b

    def __hash__(self):
        return hash(self.b)

    def __str__(self):
        return "true" if self.b else "false"

    def __eq__(self, other: "Bool") -> bool:
        return self.b == other.b

    def intersect(self, other: "Bool") -> "Bool":
        return Bool(self.b and other.b)

    def union(self, other: "Bool") -> "Bool":
        return Bool(self.b or other.b)

    def concatenate(self, other: "Bool"):
        raise NotImplementedException("Bool doesn't support '.' operation")

    def inverse(self) -> "Bool":
        return Bool(not self.b)

    def kleene(self):
        raise NotImplementedException("Bool doesn't support '*' operation")
