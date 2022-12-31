from typing import Set, Tuple

import networkx as nx
from pyformlang.cfg import Variable, CFG
from project.cfpq import _cfpq
from project.pycubool.matrix_based import matrix_based
from project.pycubool.tensor import tensor


def matrix_cfpq_cb(
        graph: nx.MultiDiGraph,
        cfg: CFG,
        start_nodes: Set[int] = None,
        final_nodes: Set[int] = None,
        start_variable: Variable = Variable("S"),
) -> Set[Tuple[int, int]]:
    cfg._start_symbol = start_variable

    return _cfpq(set(matrix_based(graph, cfg)), cfg, start_nodes, final_nodes)


def tensor_cfpq_cb(
        graph: nx.MultiDiGraph,
        cfg: CFG,
        start_nodes: Set[int] = None,
        final_nodes: Set[int] = None,
        start_variable: Variable = Variable("S"),
) -> Set[Tuple[int, int]]:
    cfg._start_symbol = start_variable

    return _cfpq(set(tensor(graph, cfg)), cfg, start_nodes, final_nodes)