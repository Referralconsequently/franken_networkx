"""Tests for drawing and visualization delegation helpers."""

from pathlib import Path

import pytest
import franken_networkx as fnx


def _path_graph():
    graph = fnx.Graph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")
    return graph


def test_draw_networkx_variants_do_not_error():
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    graph = _path_graph()
    pos = fnx.spring_layout(graph, seed=7)
    fig, ax = plt.subplots()

    try:
        fnx.draw_networkx(graph, pos=pos, ax=ax)
        fnx.draw_networkx_nodes(graph, pos=pos, ax=ax)
        fnx.draw_networkx_edges(graph, pos=pos, ax=ax)
        fnx.draw_networkx_labels(graph, pos=pos, ax=ax)
        fnx.draw_networkx_edge_labels(
            graph,
            pos=pos,
            edge_labels={("a", "b"): "ab", ("b", "c"): "bc"},
            ax=ax,
        )
        fnx.draw_forceatlas2(graph, ax=ax)
    finally:
        plt.close(fig)


def test_to_latex_variants_include_tikz_markup():
    graph = _path_graph()
    for node, coords in fnx.spring_layout(graph, seed=7).items():
        graph.nodes[node]["pos"] = tuple(coords)

    latex = fnx.to_latex(graph)
    raw = fnx.to_latex_raw(graph)

    assert "\\begin{tikzpicture}" in latex
    assert "\\begin{tikzpicture}" in raw
    assert "\\draw" in raw


def test_write_latex_and_network_text(tmp_path: Path):
    graph = _path_graph()
    for node, coords in fnx.spring_layout(graph, seed=7).items():
        graph.nodes[node]["pos"] = tuple(coords)

    latex_path = tmp_path / "graph.tex"
    text_path = tmp_path / "graph.txt"

    fnx.write_latex(graph, latex_path)
    fnx.write_network_text(graph, text_path)

    assert latex_path.read_text(encoding="utf-8")
    rendered = text_path.read_text(encoding="utf-8")
    assert "a" in rendered
    assert "b" in rendered


def test_generate_network_text_returns_lines():
    graph = _path_graph()
    lines = list(fnx.generate_network_text(graph))
    assert lines
    assert any("a" in line for line in lines)
