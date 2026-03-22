"""Tests for GEXF compatibility wrappers."""

from pathlib import Path

import franken_networkx as fnx


def _sample_graph():
    graph = fnx.DiGraph()
    graph.add_node("n0", label="Node Zero", color="red")
    graph.add_node("n1", label="Node One")
    graph.add_edge("n0", "n1", weight=2.5)
    return graph


def test_generate_and_parse_gexf_round_trip():
    graph = _sample_graph()
    gexf = "\n".join(fnx.generate_gexf(graph))
    parsed = fnx.parse_gexf(gexf)

    assert parsed.number_of_nodes() == 2
    assert parsed.number_of_edges() == 1


def test_read_and_write_gexf_round_trip(tmp_path: Path):
    graph = _sample_graph()
    path = tmp_path / "graph.gexf"

    fnx.write_gexf(graph, path)
    parsed = fnx.read_gexf(path)

    assert parsed.number_of_nodes() == 2
    assert parsed.number_of_edges() == 1


def test_relabel_gexf_graph_uses_label_attribute():
    graph = _sample_graph()
    relabeled = fnx.relabel_gexf_graph(graph)

    assert "Node Zero" in relabeled
    assert "Node One" in relabeled
