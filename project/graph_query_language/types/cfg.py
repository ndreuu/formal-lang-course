from pyformlang.cfg import CFG

from project.graph_query_language.gql_exceptions import (
    InvalidCastException,
    GQLTypeError,
    NotImplementedException,
)
from project.graph_query_language.types.automata import GQLAutomata
from project.graph_query_language.types.set import Set


class GqlCFG(GQLAutomata):
    def __init__(self, cfg: CFG):
        self.cfg = cfg

    def __str__(self):
        return self.cfg.to_text()

    @classmethod
    def fromText(cls, text: str) -> "GqlCFG":
        try:
            cfg = CFG.from_text(text=text)
            return cls(cfg=cfg)
        except ValueError as e:
            raise InvalidCastException("str", "CFG") from e

    def intersect(self, other: GQLAutomata) -> "GqlCFG":
        if not isinstance(other, GQLAutomata):
            raise GQLTypeError(
                f"Expected type FiniteAutomata, got {str(type(other))} instead."
            )

        if isinstance(other, GqlCFG):
            raise GQLTypeError("GqlCFG cannot intersect with another GqlCFG")

        intersection = self.cfg.intersection(
            other.nfa.to_deterministic()
        ).remove_useless_symbols()

        return GqlCFG(cfg=intersection)

    def union(self, other) -> "GqlCFG":
        if isinstance(other, GqlCFG):
            return GqlCFG(cfg=self.cfg.union(other.cfg))

        raise NotImplementedException("Union supported only GqlCFG types")

    def concatenate(self, other) -> "GqlCFG":
        if isinstance(other, GqlCFG):
            return GqlCFG(cfg=self.cfg.concatenate(other.cfg))

        raise NotImplementedException("Concatenate supported only GqlCFG types")

    def inverse(self):
        raise NotImplementedException("GqlCFG doesn't support inverse operation")

    def kleene(self):
        raise NotImplementedException("GqlCFG doesn't support kleene operation")

    def set_start(self, start_states):
        raise NotImplementedException(
            "Start symbol can't be set to GqlCFG after creation"
        )

    def set_final(self, final_states):
        raise NotImplementedException("Final symbol can't be set to GqlCFG")

    def add_start(self, start_states):
        raise NotImplementedException("Start symbols can't be added to GqlCFG")

    def add_final(self, final_states):
        raise NotImplementedException("Final symbols can't be added to GqlCFG")

    @property
    def start(self) -> Set:
        return Set(self.cfg.start_symbol.value)

    @property
    def final(self) -> Set:
        return Set(set(self.cfg.get_reachable_symbols()))

    @property
    def labels(self) -> Set:
        return Set(set(self.cfg.terminals))

    @property
    def edges(self) -> Set:
        raise NotImplementedException("GqlCFG edges doesn't support")

    @property
    def vertices(self) -> Set:
        return Set(set(self.cfg.variables))

    def get_reachable(self) -> Set:
        raise NotImplementedException("GqlCFG doesn't support Reachable")
