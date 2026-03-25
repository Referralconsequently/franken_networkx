"""Tests for conversion and serialization compatibility wrappers."""

import franken_networkx as fnx
import pytest


def test_pandas_adjacency_round_trip():
    pd = pytest.importorskip("pandas")

    graph = fnx.Graph()
    graph.add_edge("a", "b", weight=2.5)
    graph.add_edge("b", "c", weight=1.5)

    frame = fnx.to_pandas_adjacency(graph, dtype=float)
    restored = fnx.from_pandas_adjacency(frame)

    assert isinstance(frame, pd.DataFrame)
    assert restored["a"]["b"]["weight"] == 2.5
    assert restored["b"]["c"]["weight"] == 1.5


def test_prufer_sequence_round_trip():
    tree = fnx.path_graph(5)

    sequence = fnx.to_prufer_sequence(tree)
    restored = fnx.from_prufer_sequence(sequence)

    assert len(sequence) == 3
    assert restored.number_of_nodes() == 5
    assert restored.number_of_edges() == 4


def test_nested_tuple_round_trip():
    tree = fnx.balanced_tree(2, 2)

    nested = fnx.to_nested_tuple(tree, root=0)
    restored = fnx.from_nested_tuple(nested, sensible_relabeling=True)

    assert nested == (((), ()), ((), ()))
    assert restored.number_of_nodes() == tree.number_of_nodes()
    assert restored.number_of_edges() == tree.number_of_edges()


def test_cytoscape_and_generic_graph_conversion():
    graph = fnx.Graph()
    graph.add_edge("x", "y", weight=4)

    data = fnx.cytoscape_data(graph)
    restored = fnx.cytoscape_graph(data)
    generic = fnx.to_networkx_graph({"x": {"y": {"weight": 7}}})

    assert "elements" in data
    assert restored["x"]["y"]["weight"] == 4
    assert generic["x"]["y"]["weight"] == 7


def test_attr_sparse_matrix_returns_sparse_and_ordering():
    scipy = pytest.importorskip("scipy")

    graph = fnx.Graph()
    graph.add_node("a", color=0)
    graph.add_node("b", color=1)
    graph.add_edge("a", "b", weight=3)

    matrix, ordering = fnx.attr_sparse_matrix(graph, edge_attr="weight", node_attr="color")

    assert isinstance(matrix, scipy.sparse.sparray)
    assert ordering == [0, 1]
