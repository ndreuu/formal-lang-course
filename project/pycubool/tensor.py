import networkx as nx
from typing import Tuple, Set

from pyformlang.cfg import CFG
import pycubool as cb

from project.cfg import cfg_to_wcnf
from project.pycubool.boolean_decomposition import intersect_boolean_matrices_cb, CuBooleanMatrices
from project.regex_utils import graph_to_nfa


def tensor(graph: nx.MultiDiGraph, cfg: CFG) -> Set[Tuple[int, str, int]]:
    """
    Tensor algorithm for solving Context-Free Path Querying problem

    Parameters
    ----------
    graph: nx.MultiDiGraph
        input graph
    cfg: CFG
        input cfg

    Returns
    -------
    set[Tuple[int, str, int]]:
        set tuples (node, terminal, node)
    """
    wcnf = cfg_to_wcnf(cfg)

    n = sum(len(p.body) + 1 for p in wcnf.productions)
    rsm_heads = dict()
    nonterm = set()
    boxes = dict()
    start_states = set()
    final_states = set()
    counter = 0

    nfa_by_graph = graph_to_nfa(graph)
    bm = CuBooleanMatrices(nfa_by_graph.remove_epsilon_transitions())

    for p in wcnf.productions:
        nonterm.add(p.head.value)
        start_states.add(counter)
        final_states.add(counter + len(p.body))
        rsm_heads[(counter, counter + len(p.body))] = p.head.value
        for b in p.body:
            m = boxes.get(b.value, cb.Matrix.empty(shape=(n,n)))
            m[counter, counter + 1] = True
            boxes[b.value] = m
            counter += 1
        counter += 1

    for p in wcnf.productions:
        if len(p.body) == 0:
            tmp = cb.Matrix.empty(shape=(bm.states_count, bm.states_count))
            for i in range(bm.states_count):
              tmp[i, i] = True
            bm.bool_matrices[p.head.value] = tmp

    bfa = CuBooleanMatrices()
    bfa.start_states = start_states
    bfa.final_states = final_states
    bfa.bool_matrices = boxes
    bfa.states_count = n
    prev_nnz = -2
    new_nnz = -1
    while prev_nnz != new_nnz:
        transitive_closure = intersect_boolean_matrices_cb(
            bfa, bm
        ).make_transitive_closure()
        prev_nnz, new_nnz = new_nnz, transitive_closure.nvals
        x, y = transitive_closure.to_lists()

        for (i, j) in zip(x, y):
            rfa_from = i // bm.states_count
            rfa_to = j // bm.states_count
            graph_from = i % bm.states_count
            graph_to = j % bm.states_count

            if (rfa_from, rfa_to) not in rsm_heads:
                continue

            variable = rsm_heads[(rfa_from, rfa_to)]
            m = bm.bool_matrices.get(
                variable,
                cb.Matrix.empty(shape=(bm.states_count, bm.states_count)),
            )
            m[graph_from, graph_to] = True
            bm.bool_matrices[variable] = m

    return {
        (u, key, v)
        for key, m in bm.bool_matrices.items()
        if key in nonterm
        for (u, v) in zip(*m.to_lists())
    }



# from pycubool import Matrix
#
# from networkx import Graph
# from pyformlang.cfg import CFG, Variable
# from project.pycubool.boolean_decomposition import BooleanDecomposition
#
# from project.regex_utils import create_nfa_from_graph
# from project.rsm import RSM
# from project.ecfg import ECFG
#
#
# def tensor(graph: Graph, cfg: CFG) -> set[tuple[int, Variable, int]]:
#     graph_matrix = BooleanDecomposition.from_nfa(create_nfa_from_graph(graph))
#     rsm = RSM.from_ecfg((ECFG.from_cfg(cfg))).minimize()
#     rsm_matrix = BooleanDecomposition.from_rsm(rsm)
#     # from_nfa(rsm.rsm_to_single_NFA())
#
#     identity_matrix = Matrix.empty(
#         shape=(len(graph_matrix.state_indices.keys()), len(graph_matrix.state_indices.keys()))
#     )
#     for i in range(len(graph_matrix.state_indices.keys())):
#         identity_matrix[i, i] = True
#
#     for var in cfg.get_nullable_symbols():
#         if var.value in graph_matrix.bool_decomposition.keys():
#             graph_matrix.bool_decomposition[var.value] += identity_matrix
#         else:
#             graph_matrix.bool_decomposition[var.value] = identity_matrix
#
#     last = 0
#     while True:
#         tc_idxs = list(
#             zip(*rsm_matrix & graph_matrix.make_transitive_closure().to_lists())
#         )
#         if len(tc_idxs) == last:
#             break
#         last = len(tc_idxs)
#         for (i, j) in tc_idxs:
#             r_i, r_j = i // len(graph_matrix.state_indices.keys()), j // len(graph_matrix.state_indices.keys())
#             g_i, g_j = (
#                 i % len(graph_matrix.state_indices.keys()),
#                 j % len(graph_matrix.state_indices.keys()),
#             )
#
#             state_from = rsm_matrix.state_indices[r_i]
#             state_to = rsm_matrix.state_indices[r_j]
#             var, _ = state_from.value
#             if (
#                 state_from in rsm_matrix.start_states
#                 and state_to in rsm_matrix.final_states
#             ):
#                 if var.value in graph_matrix.bool_decomposition.keys():
#                     graph_matrix.bool_decomposition[var][g_i, g_j] = True
#                 else:
#                     graph_matrix.bool_decomposition[var] = Matrix.empty(
#                         shape=(len(graph_matrix.state_indices.keys()), len(graph_matrix.state_indices.keys()))
#                     )
#                     graph_matrix.bool_decomposition[var][g_i, g_j] = True
#
#     result = set()
#     for variable, matrix in graph_matrix.bool_decomposition.items():
#         for u, v in zip(*matrix.to_lists()):
#             result.add(
#                 (graph_matrix.state_indices[u], variable, graph_matrix.state_indices[v])
#             )
#
#     return result
