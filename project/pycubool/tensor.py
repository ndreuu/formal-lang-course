from pycubool import Matrix

from networkx import Graph
from pyformlang.cfg import CFG, Variable
from project.pycubool.boolean_decomposition import BooleanDecomposition

from project.regex_utils import create_nfa_from_graph
from project.rsm import RSM
from project.ecfg import ECFG


def tensor(graph: Graph, cfg: CFG) -> set[tuple[int, Variable, int]]:
    graph_matrix = BooleanDecomposition.from_nfa(create_nfa_from_graph(graph))
    rsm = RSM.from_ecfg((ECFG.from_cfg(cfg))).minimize()
    rsm_matrix = BooleanDecomposition.from_nfa(rsm.rsm_to_single_NFA())

    identity_matrix = Matrix.empty(
        shape=(len(graph_matrix.state_indices.keys()), len(graph_matrix.state_indices.keys()))
    )
    for i in range(len(graph_matrix.state_indices.keys())):
        identity_matrix[i, i] = True

    for var in cfg.get_nullable_symbols():
        if var.value in graph_matrix.bool_decomposition.keys():
            graph_matrix.bool_decomposition[var.value] += identity_matrix
        else:
            graph_matrix.bool_decomposition[var.value] = identity_matrix

    last = 0
    while True:
        tc_idxs = list(
            zip(*rsm_matrix & graph_matrix.make_transitive_closure().to_lists())
        )
        if len(tc_idxs) == last:
            break
        last = len(tc_idxs)
        for (i, j) in tc_idxs:
            r_i, r_j = i // len(graph_matrix.state_indices.keys()), j // len(graph_matrix.state_indices.keys())
            g_i, g_j = (
                i % len(graph_matrix.state_indices.keys()),
                j % len(graph_matrix.state_indices.keys()),
            )

            state_from = rsm_matrix.state_indices[r_i]
            state_to = rsm_matrix.state_indices[r_j]
            var, _ = state_from.value
            if (
                state_from in rsm_matrix.start_states
                and state_to in rsm_matrix.final_states
            ):
                if var.value in graph_matrix.bool_decomposition.keys():
                    graph_matrix.bool_decomposition[var][g_i, g_j] = True
                else:
                    graph_matrix.bool_decomposition[var] = Matrix.empty(
                        shape=(len(graph_matrix.state_indices.keys()), len(graph_matrix.state_indices.keys()))
                    )
                    graph_matrix.bool_decomposition[var][g_i, g_j] = True

    result = set()
    for variable, matrix in graph_matrix.bool_decomposition.items():
        for u, v in zip(*matrix.to_lists()):
            result.add(
                (graph_matrix.state_indices[u], variable, graph_matrix.state_indices[v])
            )

    return result
