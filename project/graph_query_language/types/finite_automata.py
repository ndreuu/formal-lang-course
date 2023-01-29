from enum import Enum, auto
from typing import Any

import networkx as nx
from pyformlang.regular_expression import MisformedRegexError

from project.boolean_decompositonNFA import BooleanDecompositionNFA
from project.graph_query_language.gql_exceptions import (
    GQLTypeError,
    InvalidCastException,
)
from project.graph_query_language.types.automata import GQLAutomata
from project.graph_query_language.types.cfg import GqlCFG
from project.graph_query_language.types.set import Set
from project.graph_utils import add_states_to_nfa, replace_nfa_states
from project.regex_utils import regex_to_dfa
from project.rpq import get_reachable
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)


class Arity(Enum):
    Un = auto()
    Bin = auto()


class FiniteGQLAutomata(GQLAutomata):
    is_from_str = False

    def __init__(self, nfa: NondeterministicFiniteAutomaton):
        self.nfa = nfa
        self.is_from_str = False

    def __str__(self):
        return str(self.nfa.to_deterministic().minimize().to_regex())

    @staticmethod
    def apply_f(self, arity: Arity, other: Any, f) -> GQLAutomata | None:
        if arity == Arity.Un:
            result = f()
            result.is_from_str = self.is_from_str
            return result
        else:
            result = f(other)
            result.is_from_str = self.is_from_str and other.is_from_str
            return result

    @classmethod
    def get_nfa(cls):
        return cls.nfa

    @staticmethod
    def __get_reachable(nfa: NondeterministicFiniteAutomaton) -> set:
        bmatrix = BooleanDecompositionNFA(nfa.remove_epsilon_transitions())
        return get_reachable(bmatrix)

    @classmethod
    def fromGraph(cls, graph: nx.Graph) -> "FiniteGQLAutomata":
        return cls(nfa=nfa_from_graph(graph, set(), set()))

    @classmethod
    def fromString(cls, regex_str: str) -> "FiniteGQLAutomata":
        try:
            fa = FiniteGQLAutomata(nfa=regex_to_dfa(regex_str))
            fa.is_from_str = True
            return fa
        except MisformedRegexError as exc:
            raise InvalidCastException("str", "regex") from exc

    def __intersectFiniteAutomata(
        self, other: "FiniteGQLAutomata"
    ) -> "FiniteGQLAutomata":
        lhs = BooleanDecompositionNFA(self.nfa.remove_epsilon_transitions())
        rhs = BooleanDecompositionNFA(other.nfa.remove_epsilon_transitions())
        intersection_result = lhs.get_intersect_boolean_decomposition(rhs)
        return FiniteGQLAutomata(
            nfa=intersection_result.decomposition_to_automaton(),
        )

    def __intersectCFG(self, other: GqlCFG) -> GqlCFG:
        intersection = other.intersect(self)
        return intersection

    def _intersect(self, other) -> "GQLAutomata":
        if isinstance(other, FiniteGQLAutomata):
            return self.__intersectFiniteAutomata(other=other)

        if isinstance(other, GqlCFG):
            if self.is_from_str:
                raise GQLTypeError(f"For intersect cfg with fa, define fa from graph")
            else:
                return self.__intersectCFG(other=other)

        raise GQLTypeError(
            f"Expected type BaseAutomata, got {str(type(other))} instead."
        )

    def intersect(self, other) -> "GqlCFG":
        return self.apply_f(self, Arity.Bin, other, self._intersect)

    def _union(self, other: "FiniteGQLAutomata") -> "FiniteGQLAutomata":
        return FiniteGQLAutomata(self.nfa.union(other.nfa).to_deterministic())

    def union(self, other: "FiniteGQLAutomata") -> "FiniteGQLAutomata":
        return self.apply_f(self, Arity.Bin, other, self._union)

    def _concatenate(self, other: "FiniteGQLAutomata") -> "FiniteGQLAutomata":
        lhs = self.nfa.to_regex()
        rhs = other.nfa.to_regex()
        fa = FiniteGQLAutomata(lhs.concatenate(rhs).to_epsilon_nfa().to_deterministic())
        return fa

    def concatenate(self, other: "FiniteGQLAutomata") -> "FiniteGQLAutomata":
        return self.apply_f(self, Arity.Bin, other, self._concatenate)

    def _inverse(self) -> "FiniteGQLAutomata":
        return FiniteGQLAutomata(self.nfa.get_complement().to_deterministic())

    def inverse(self) -> "FiniteGQLAutomata":
        return self.apply_f(self, None, self, self._inverse)

    def _kleene(self) -> "FiniteGQLAutomata":
        return FiniteGQLAutomata(nfa=self.nfa.kleene_star().to_deterministic())

    def kleene(self) -> "FiniteGQLAutomata":
        return self.apply_f(self, Arity.Un, None, self._kleene)

    @property
    def start(self) -> Set:
        return Set(self.nfa.start_states)

    @property
    def final(self) -> Set:
        return Set(self.nfa.final_states)

    @property
    def labels(self) -> Set:
        return Set(self.nfa.symbols)

    @property
    def edges(self) -> Set:
        edges_dict = self.nfa.to_dict()
        edges_set = set()
        for u in edges_dict.keys():
            for label, v_s in edges_dict.get(u).items():
                for v in v_s:
                    edges_set.add((u, label, v))
        return Set(edges_set)

    @property
    def vertices(self) -> Set:
        return Set(self.nfa.states)

    def set_start(self, start_states: Set) -> "FiniteGQLAutomata":
        nfa = replace_nfa_states(self.nfa, start_states=start_states.data)
        return FiniteGQLAutomata(nfa)

    def set_final(self, final_states: Set) -> "FiniteGQLAutomata":
        nfa = replace_nfa_states(self.nfa, final_states=final_states.data)
        return FiniteGQLAutomata(nfa)

    def add_start(self, start_states: Set) -> "FiniteGQLAutomata":
        nfa = add_states_to_nfa(self.nfa, start_states=start_states.data)
        return FiniteGQLAutomata(nfa)

    def add_final(self, final_states: Set) -> "FiniteGQLAutomata":
        nfa = add_states_to_nfa(self.nfa, final_states=final_states.data)
        return FiniteGQLAutomata(nfa)

    def get_reachable(self) -> Set:
        return Set(FiniteGQLAutomata.__get_reachable(self.nfa))


def nfa_from_graph(
    graph: nx.Graph, start_states: set[int] = None, final_states: set[int] = None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for statement_from, statement_to, transition in graph.edges(data=True):
        nfa.add_transition(
            State(int(statement_from)),
            Symbol(transition["label"]),
            State(int(statement_to)),
        )

    for node in map(lambda node: int(node), graph.nodes):
        if start_states == None or node in map(lambda state: int(state), start_states):
            nfa.add_start_state(State(node))
        if final_states == None or node in map(lambda state: int(state), final_states):
            nfa.add_final_state(State(node))

    return nfa
