from abc import ABC, abstractmethod
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from project.graph_query_language.types.gql_type import GQLType


class GQLAutomata(GQLType, ABC):
    nfa: NondeterministicFiniteAutomaton = None

    @property
    @abstractmethod
    def start(self):
        pass

    @property
    @abstractmethod
    def final(self):
        pass

    @property
    @abstractmethod
    def labels(self):
        pass

    @property
    @abstractmethod
    def edges(self):
        pass

    @property
    @abstractmethod
    def vertices(self):
        pass

    @abstractmethod
    def set_start(self, start_states):
        pass

    @abstractmethod
    def set_final(self, final_states):
        pass

    @abstractmethod
    def add_start(self, start_states):
        pass

    @abstractmethod
    def add_final(self, final_states):
        pass

    @abstractmethod
    def get_reachable(self):
        pass
