from project.graph_query_language.gql_exceptions import (
    GQLTypeError,
    NotImplementedException,
)
from project.graph_query_language.types.gql_type import GQLType
from project.graph_query_language.types.bool import Bool


class Set(GQLType):
    def __init__(self, internal_set: set):
        self._type = Set.get_type(internal_set)
        self._set = internal_set

    def __str__(self):
        return "{" + ", ".join(map(lambda x: str(x), self.data)) + "}"

    @staticmethod
    def get_type(set_obj: set) -> type:
        if len(set_obj) == 0:
            return type(None)
        iseq = iter(set_obj)
        return type(next(iseq))

    @staticmethod
    def _check_type_consistency(set_obj: set) -> bool:
        if len(set_obj) == 0:
            return True
        iseq = iter(set_obj)
        t = type(next(iseq))
        return all(map(lambda x: isinstance(x, t), iseq))

    @classmethod
    def fromSet(cls, pyset: set) -> "Set":
        if not Set._check_type_consistency(pyset):
            raise GQLTypeError("Type consistency failed")
        return Set(pyset)

    @property
    def set_type(self) -> type:
        return self._type

    @property
    def data(self) -> set:
        return self._set

    def __len__(self):
        return len(self._set)

    def find(self, value) -> Bool:
        return Bool(value in self._set)

    def intersect(self, other: "Set") -> "Set":
        if self.data and other.data and self.set_type != other.set_type:
            raise GQLTypeError(f"Types mismatched: {self.set_type} != {other.set_type}")
        return Set(internal_set=self.data & other.data)

    def union(self, other: "Set") -> "Set":
        if self.data and other.data and self.set_type != other.set_type:
            raise GQLTypeError(f"Types mismatched: {self.set_type} != {other.set_type}")
        return Set(internal_set=self.data | other.data)

    def concatenate(self, other):
        raise NotImplementedException("Set doesn't support '.' operation, use |")

    def inverse(self):
        raise NotImplementedException("Set doesn't support 'not' operation")

    def kleene(self):
        raise NotImplementedException("Set doesn't support '*' operation")
