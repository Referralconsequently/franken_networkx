"""Tests for graph utility wrapper functions."""

import networkx as nx

import franken_networkx as fnx
from franken_networkx.drawing.layout import _to_nx


def test_voronoi_cells_and_stoer_wagner_match_networkx():
    graph = fnx.path_graph(5)

    assert fnx.voronoi_cells(graph, [0, 4]) == nx.voronoi_cells(nx.path_graph(5), [0, 4])
    assert fnx.stoer_wagner(graph) == nx.stoer_wagner(nx.path_graph(5))


def test_dedensify_and_quotient_graph_match_networkx():
    bipartite = fnx.complete_bipartite_graph(2, 4)
    dedensified, compressors = fnx.dedensify(bipartite, 2, prefix="aux")
    dedensified_nx, compressors_nx = nx.dedensify(_to_nx(bipartite), 2, prefix="aux")

    partition = [{0, 1}, {2, 3}]
    quotient = fnx.quotient_graph(fnx.path_graph(4), partition)
    quotient_nx = nx.quotient_graph(_to_nx(fnx.path_graph(4)), partition)

    assert sorted(_to_nx(dedensified).edges()) == sorted(dedensified_nx.edges())
    assert compressors == compressors_nx
    assert sorted(_to_nx(quotient).edges()) == sorted(quotient_nx.edges())


def test_snap_aggregation_and_full_join_match_networkx():
    graph = fnx.path_graph(4)
    for node, color in [(0, "red"), (1, "red"), (2, "blue"), (3, "blue")]:
        graph.nodes[node]["color"] = color

    graph_nx = nx.path_graph(4)
    for node, color in [(0, "red"), (1, "red"), (2, "blue"), (3, "blue")]:
        graph_nx.nodes[node]["color"] = color

    summary = fnx.snap_aggregation(graph, ["color"])
    summary_nx = nx.snap_aggregation(graph_nx, ["color"])
    joined = fnx.full_join(fnx.path_graph(2), fnx.path_graph(2), rename=("L", "R"))
    joined_nx = nx.full_join(nx.path_graph(2), nx.path_graph(2), rename=("L", "R"))

    assert sorted(_to_nx(summary).edges()) == sorted(summary_nx.edges())
    assert sorted(_to_nx(joined).edges()) == sorted(joined_nx.edges())


def test_identified_nodes_and_inverse_line_graph_match_networkx():
    path = fnx.path_graph(4)
    identified = fnx.identified_nodes(path, 1, 2)
    identified_nx = nx.identified_nodes(_to_nx(path), 1, 2)

    line = fnx.line_graph(fnx.path_graph(5))
    inverse = fnx.inverse_line_graph(line)
    inverse_nx = nx.inverse_line_graph(_to_nx(line))

    assert sorted(_to_nx(identified).edges()) == sorted(identified_nx.edges())
    assert sorted(_to_nx(inverse).edges()) == sorted(inverse_nx.edges())
