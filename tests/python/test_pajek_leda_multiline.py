"""Tests for Pajek, LEDA, and multiline adjacency-list wrappers."""

from pathlib import Path

import franken_networkx as fnx


def test_generate_and_parse_pajek_round_trip():
    graph = fnx.Graph()
    graph.add_edge("a", "b", weight=2.5)

    lines = list(fnx.generate_pajek(graph))
    parsed = fnx.parse_pajek(lines)

    assert parsed.number_of_nodes() == 2
    assert parsed.number_of_edges() == 1
    assert parsed["a"]["b"][0]["weight"] == 2.5


def test_read_and_write_pajek_round_trip(tmp_path: Path):
    graph = fnx.Graph()
    graph.add_edge("left", "right", weight=1.25)
    path = tmp_path / "graph.net"

    fnx.write_pajek(graph, path)
    parsed = fnx.read_pajek(path)

    assert parsed.number_of_nodes() == 2
    assert parsed.number_of_edges() == 1
    assert parsed["left"]["right"][0]["weight"] == 1.25


def test_parse_leda_sample():
    lines = [
        "LEDA.GRAPH",
        "string",
        "int",
        "-2",
        "2",
        "|{a}|",
        "|{b}|",
        "1",
        "1 2 0 |{5}|",
    ]

    parsed = fnx.parse_leda(lines)

    assert parsed.number_of_nodes() == 2
    assert parsed.number_of_edges() == 1
    assert parsed["a"]["b"]["label"] == "5"


def test_multiline_adjlist_round_trip(tmp_path: Path):
    graph = fnx.Graph()
    graph.add_edge("a", "b")
    graph.add_node("solo")

    lines = list(fnx.generate_multiline_adjlist(graph))
    parsed = fnx.parse_multiline_adjlist(lines)
    path = tmp_path / "graph.adj"

    fnx.write_multiline_adjlist(graph, path)
    from_file = fnx.read_multiline_adjlist(path)

    assert parsed.number_of_nodes() == 3
    assert parsed.number_of_edges() == 1
    assert "solo" in parsed
    assert from_file.number_of_nodes() == 3
    assert from_file.number_of_edges() == 1
    assert "solo" in from_file
