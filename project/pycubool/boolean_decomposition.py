import pycubool as cb
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

class CuBooleanMatrices:
    def __init__(self, n_automaton: NondeterministicFiniteAutomaton = None):
        if n_automaton is None:
            self.states_count = 0
            self.state_indices = dict()
            self.start_states = set()
            self.final_states = set()
            self.bool_matrices = dict()
        else:
            self.states_count = len(n_automaton.states)
            self.state_indices = {
                state: index for index, state in enumerate(n_automaton.states)
            }
            self.start_states = n_automaton.start_states
            self.final_states = n_automaton.final_states
            self.bool_matrices = self.init_bool_matrices(n_automaton)

    def get_states(self):
        return self.state_indices.keys()

    def get_start_states(self):
        return self.start_states

    def get_final_states(self):
        return self.final_states

    def init_bool_matrices(self, n_automaton: NondeterministicFiniteAutomaton):
        """
        Initialize boolean matrices of NondeterministicFiniteAutomaton

        Parameters
        ----------
        n_automaton: NondeterministicFiniteAutomaton
            NFA to transform to matrix

        Returns
        -------
        bool_matrices: dict
            Dict of boolean matrix for every automata label-key
        """
        bool_matrices = dict()
        nfa_dict = n_automaton.to_dict()
        for state_from, trans in nfa_dict.items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    index_from = self.state_indices[state_from]
                    index_to = self.state_indices[state_to]
                    if label not in bool_matrices:
                        bool_matrices[label] = cb.Matrix.empty(shape=(self.states_count, self.states_count))
                    bool_matrices[label][index_from, index_to] = True

        return bool_matrices

    def make_transitive_closure(self):
        """
        Makes transitive closure of boolean matrices

        Returns
        -------
        tc: cuBool matrix
            Transitive closure of boolean matrices
        """
        if not self.bool_matrices.values():
            return cb.Matrix.empty(shape=(2, 2))

        shape = list(self.bool_matrices.values())[0].shape
        tc = cb.Matrix.empty(shape=shape)

        for elem in self.bool_matrices.values():
            tc = tc.ewiseadd(elem)
        prev_nnz = tc.nvals
        curr_nnz = 0

        while prev_nnz != curr_nnz:
            tc = tc.ewiseadd(tc.mxm(tc))
            prev_nnz, curr_nnz = curr_nnz, tc.nvals


        return tc




def intersect_boolean_matrices_cb(self: CuBooleanMatrices, other: CuBooleanMatrices):
    """
    Makes intersection of self boolean matrix with other

    Parameters
    ----------
    self: CuBooleanMatrices
        Left-hand side boolean matrix
    other: CuBooleanMatrices
        Right-hand side boolean matrix

    Returns
    -------
    intersect_bm: CuBooleanMatrices
        Intersection of two boolean matrices
    """
    intersect_bm = CuBooleanMatrices()
    intersect_bm.num_states = self.states_count * other.states_count
    common_symbols = self.bool_matrices.keys() & other.bool_matrices.keys()

    for symbol in common_symbols:
        intersect_bm.bool_matrices[symbol] = self.bool_matrices[symbol].kronecker(other.bool_matrices[symbol])

    for state_fst, state_fst_index in self.state_indices.items():
        for state_snd, state_snd_idx in other.state_indices.items():
            new_state = new_state_idx = (
                    state_fst_index * other.states_count + state_snd_idx
            )
            intersect_bm.state_indices[new_state] = new_state_idx

            if state_fst in self.start_states and state_snd in other.start_states:
                intersect_bm.start_states.add(new_state)

            if state_fst in self.final_states and state_snd in other.final_states:
                intersect_bm.final_states.add(new_state)

    return intersect_bm

# from collections import defaultdict
# from pyformlang.finite_automaton import State, EpsilonNFA
# from project.rsm import RSM
#
# from pycubool import Matrix
#
#
# class BooleanDecomposition:
#     def __init__(
#         self,
#         state_indices: dict,
#         start_states: set,
#         final_states: set,
#         bool_decomposition: dict[any, Matrix],
#     ):
#         self.state_indices = state_indices
#         self.start_states = start_states
#         self.final_states = final_states
#         self.bool_decomposition = bool_decomposition
#
#     def __and__(self, other: "BooleanDecomposition") -> "BooleanDecomposition":
#         inter_labels = self.bool_decomposition.keys() & other.bool_decomposition.keys()
#         inter_bool_matrices = {
#             label: self.bool_decomposition[label].kronecker(other.bool_decomposition[label])
#             for label in inter_labels
#         }
#         inter_states_indices = dict()
#         inter_start_states = set()
#         inter_final_states = set()
#         for self_state, self_idx in self.state_indices.items():
#             for other_state, other_idx in other.state_indices.items():
#                 state = State((self_state.value, other_state.value))
#                 idx = self_idx * len(other.state_indices) + other_idx
#                 inter_states_indices[state] = idx
#                 if (
#                     self_state in self.start_states
#                     and other_state in other.start_states
#                 ):
#                     inter_start_states.add(state)
#                 if (
#                     self_state in self.final_states
#                     and other_state in other.final_states
#                 ):
#                     inter_final_states.add(state)
#         return BooleanDecomposition(
#             inter_states_indices,
#             inter_start_states,
#             inter_final_states,
#             inter_bool_matrices,
#         )
#
#     def to_nfa(self) -> EpsilonNFA:
#         nfa = EpsilonNFA()
#         for label, matrix in self.bool_decomposition.items():
#             matrix_as_array = Matrix.to_list()
#             for state_from, i in self.state_indices.items():
#                 for state_to, j in self.state_indices.items():
#                     if matrix_as_array[i][j]:
#                         nfa.add_transitions([(state_from, label, state_to)])
#
#         for state in self.start_states:
#             nfa.add_start_state(state)
#         for state in self.final_states:
#             nfa.add_final_state(state)
#
#         return nfa
#
#     def get_start_states(self) -> set[State]:
#         return self.start_states.copy()
#
#     def get_final_states(self) -> set[State]:
#         return self.final_states.copy()
#
#     def make_transitive_closure(self) -> Matrix:
#         transitive_closure = sum(
#             self.bool_decomposition.values(),
#             start=Matrix.empty((len(self.state_indices), len(self.state_indices))),
#         )
#         cur_nnz = transitive_closure.nnz
#         prev_nnz = None
#
#         if not cur_nnz:
#             return transitive_closure
#
#         while prev_nnz != cur_nnz:
#             transitive_closure += transitive_closure @ transitive_closure
#             prev_nnz, cur_nnz = cur_nnz, transitive_closure.nnz
#
#         return transitive_closure
#
#     @classmethod
#     def from_nfa(cls, nfa: EpsilonNFA) -> "BooleanDecomposition":
#         state_to_index = {state: index for index, state in enumerate(nfa.states)}
#         return cls(
#             state_indices=state_to_index,
#             start_states=nfa.start_states.copy(),
#             final_states=nfa.final_states.copy(),
#             bool_decomposition=cls._create_boolean_matrix_from_nfa(
#                 nfa=nfa, state_to_index=state_to_index
#             ),
#         )
#
#     @classmethod
#     def from_rsm(cls, rsm: RSM) -> "BooleanDecomposition":
#         states, start_states, final_states = set(), set(), set()
#         for nonterm, dfa in rsm.boxes.items():
#             for s in dfa.states:
#                 state = State((nonterm, s.value))
#                 states.add(state)
#                 if s in dfa.start_states:
#                     start_states.add(state)
#                 if s in dfa.final_states:
#                     final_states.add(state)
#         states = sorted(states, key=lambda s: s.value)
#         state_to_idx = {s: i for i, s in enumerate(states)}
#         b_mtx = defaultdict(lambda: Matrix.empty((len(states), len(states))))
#         for nonterm, dfa in rsm.boxes.items():
#             for state_from, transitions in dfa.to_dict().items():
#                 for label, states_to in transitions.items():
#                     mtx = b_mtx[label.value]
#                     states_to = states_to if isinstance(states_to, set) else {states_to}
#                     for state_to in states_to:
#                         mtx[
#                             state_to_idx[State((nonterm, state_from.value))],
#                             state_to_idx[State((nonterm, state_to.value))],
#                         ] = True
#         return cls(
#             state_to_idx,
#             start_states,
#             final_states,
#             b_mtx,
#         )
#
#     @staticmethod
#     def _create_boolean_matrix_from_nfa(
#         nfa: EpsilonNFA, state_to_index: dict[State, int]
#     ) -> dict[any, Matrix]:
#         boolean_matrices = defaultdict(
#             lambda: Matrix.empty((len(nfa.states), len(nfa.states)))
#         )
#         state_from_to_transition = nfa.to_dict()
#         for label in nfa.symbols:
#             dok_mtx = Matrix.empty((len(nfa.states), len(nfa.states)))
#             for state_from, transitions in state_from_to_transition.items():
#                 states_to = transitions.get(label, set())
#                 if not isinstance(states_to, set):
#                     states_to = {states_to}
#                 for state_to in states_to:
#                     dok_mtx[state_to_index[state_from], state_to_index[state_to]] = True
#             boolean_matrices[label] = dok_mtx
#         return boolean_matrices
