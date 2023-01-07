import cfpq_data
import networkx.drawing.nx_pydot
import pydot
from networkx import MultiDiGraph

from project.graph_query_language.gql_exceptions import LoadGraphException

import networkx as nx

from project.graph_query_language.types.finite_automata import FiniteGQLAutomata


def read_graph(path: str) -> FiniteGQLAutomata:
    dot_graph = pydot.graph_from_dot_file(path)[0]
    graph: nx.Graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)
    return FiniteGQLAutomata.fromGraph(graph)


def get_graph(name) -> MultiDiGraph:
    data = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(data)

    return graph


def get_graph_by_name(name: str) -> FiniteGQLAutomata:
    try:
        graph = get_graph(name)
    except Exception as exc:
        raise LoadGraphException(name=name) from exc

    return FiniteGQLAutomata.fromGraph(graph)
