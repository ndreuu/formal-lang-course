import cfpq_data
import networkx
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

from project.graph_info import GraphInfo


def get_graph_info(graph):
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set([edge[2]["label"] for edge in graph.edges(data=True)]),
    )


def get_graph_info_by_name(name):
    try:
        data = cfpq_data.download(name)
        graph = cfpq_data.graph_from_csv(data)
    except FileNotFoundError:
        raise ValueError(f"Wrong name, graph {name} doesn't exist")
    return get_graph_info(graph)


def generate_two_cycles_graph(num_of_fst_cycle_nodes, num_of_snd_cycle_nodes, path):
    if num_of_fst_cycle_nodes <= 0 or num_of_snd_cycle_nodes <= 0:
        raise ValueError("Wrong numbers of nodes in cycle(s)")
    graph = cfpq_data.labeled_two_cycles_graph(
        num_of_fst_cycle_nodes, num_of_snd_cycle_nodes, labels=["a", "b"]
    )

    networkx.drawing.nx_pydot.write_dot(graph, path)


def add_states_to_nfa(
    nfa: NondeterministicFiniteAutomaton,
    start_states: set = None,
    final_states: set = None,
) -> NondeterministicFiniteAutomaton:
    new_nfa = nfa.copy()

    if start_states:
        for state in start_states:
            new_nfa.add_start_state(state)

    if final_states:
        for state in final_states:
            new_nfa.add_final_state(state)

    return new_nfa


def replace_nfa_states(
    nfa: NondeterministicFiniteAutomaton,
    start_states: set = None,
    final_states: set = None,
) -> NondeterministicFiniteAutomaton:
    new_nfa = nfa.copy()
    new_nfa._start_states = set()
    new_nfa._final_states = set()

    if start_states:
        for state in start_states:
            new_nfa.add_start_state(state)

    if final_states:
        for state in final_states:
            new_nfa.add_final_state(state)

    return new_nfa
