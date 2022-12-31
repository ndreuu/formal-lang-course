import networkx as nx
import pyformlang.cfg as c
from project.cfg import cfg_to_wcnf
from pycubool import Matrix


from project.ecfg import ECFG
# from project.wcnf_utils import convert_cfg_to_wcnf
# from project.rsm_utils import convert_ecfg_to_rsm
# from project.graph_funcs import get_nfa_by_graph
from networkx import MultiDiGraph
from pyformlang.cfg import CFG

import pycubool as cb

def matrix_based(graph: nx.Graph, cfg: CFG):
    wcnf = cfg_to_wcnf(cfg)

    eps_prod_heads = [p.head.value for p in wcnf.productions if not p.body]
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}
    nodes_num = graph.number_of_nodes()
    matrices = {
        v.value: cb.Matrix.empty(shape=(nodes_num, nodes_num)) for v in wcnf.variables
    }

    for i, j, data in graph.edges(data=True):
        l = data["label"]
        for v in {p.head.value for p in term_productions if p.body[0].value == l}:
            matrices[v][i, j] = True

    for i in range(nodes_num):
        for v in eps_prod_heads:
            matrices[v][i, i] = True

    any_changing = True
    while any_changing:
        any_changing = False
        for p in var_productions:
            old_nnz = set(matrices[p.head.value].to_list())
            matrices[p.head.value] = matrices[p.head.value].ewiseadd(
                matrices[p.body[0].value].mxm(matrices[p.body[1].value])
            )
            new_nnz = set(matrices[p.head.value].to_list())
            any_changing = any_changing or old_nnz != new_nnz

    return {
        (u, variable, v)
        for variable, matrix in matrices.items()
        for u, v in matrix.to_list()
    }


# def matrix_based(graph: nx.Graph, cfg: c.CFG) -> set[tuple[int, c.Variable, int]]:
#     nodes_num = graph.number_of_nodes()
#     if nodes_num == 0:
#         return set()
#
#     terminal_productions = set()
#     var_productions = set()
#     eps_productions = set()
#
#     cfg = cfg_to_wcnf(cfg)
#
#     for p in cfg.productions:
#         if len(p.body) == 1:
#             terminal_productions.add(p)
#         elif len(p.body) == 2:
#             var_productions.add(p)
#         else:
#             eps_productions.add(p.head.value)
#
#     matrices = {}
#     for v in cfg.variables:
#         matrices[v.value] = Matrix.empty(shape=(nodes_num, nodes_num))
#
#     for u, v, ddict in graph.edges(data=True):
#         for p in terminal_productions:
#             if ddict["label"] == p.body[0].value:
#                 matrices[p.head.value][u, v] = True
#
#     for i in range(nodes_num):
#         for var in eps_productions:
#             matrices[var][i, i] = True
#
#     changed = True
#     while changed:
#         changed = False
#         for p in var_productions:
#             old_nnz = matrices[p.head.value].nvals
#             matrices.get(p.body[0].value, Matrix.empty((nodes_num, nodes_num))).mxm(
#                 matrices.get(p.body[1].value, Matrix.empty((nodes_num, nodes_num))),
#                 out=matrices[p.head.value],
#                 accumulate=True,
#             )
#             new_nnz = matrices[p.head.value].nvals
#             changed = old_nnz != new_nnz
#
#     result = set()
#     for variable, matrix in matrices.items():
#         for u, v in zip(*matrix.to_lists()):
#             result.add((u, variable, v))
#     return result
