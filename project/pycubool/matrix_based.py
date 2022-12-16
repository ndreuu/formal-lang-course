import networkx as nx
import pyformlang.cfg as c
from project.cfg import cfg_to_wcnf
from pycubool import Matrix


def matrix_based(graph: nx.Graph, cfg: c.CFG) -> set[tuple[int, c.Variable, int]]:
    nodes_num = graph.number_of_nodes()
    if nodes_num == 0:
        return set()

    terminal_productions = set()
    var_productions = set()
    eps_productions = set()

    cfg = cfg_to_wcnf(cfg)

    for p in cfg.productions:
        if len(p.body) == 1:
            terminal_productions.add(p)
        elif len(p.body) == 2:
            var_productions.add(p)
        else:
            eps_productions.add(p.head.value)

    matrices = {}
    for v in cfg.variables:
        matrices[v.value] = Matrix.empty(shape=(nodes_num, nodes_num))

    for u, v, ddict in graph.edges(data=True):
        for p in terminal_productions:
            if ddict["label"] == p.body[0].value:
                matrices[p.head.value][u, v] = True

    for i in range(nodes_num):
        for var in eps_productions:
            matrices[var][i, i] = True

    changed = True
    while changed:
        changed = False
        for p in var_productions:
            old_nnz = matrices[p.head.value].nvals
            matrices.get(p.body[0].value, Matrix.empty((nodes_num, nodes_num))).mxm(
                matrices.get(p.body[1].value, Matrix.empty((nodes_num, nodes_num))),
                out=matrices[p.head.value],
                accumulate=True,
            )
            new_nnz = matrices[p.head.value].nvals
            changed = old_nnz != new_nnz

    result = set()
    for variable, matrix in matrices.items():
        for u, v in zip(*matrix.to_lists()):
            result.add((u, variable, v))
    return result
