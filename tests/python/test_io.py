"""Tests for I/O functions: read/write_edgelist, read/write_adjlist,
read/write_graphml, node_link_data/graph."""

import io
import os
import tempfile

import pytest

import franken_networkx as fnx


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def triangle():
    G = fnx.Graph()
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(0, 2)
    return G


@pytest.fixture
def weighted_graph():
    G = fnx.Graph()
    G.add_edge(0, 1, weight=1.5)
    G.add_edge(1, 2, weight=2.5)
    return G


@pytest.fixture
def small_digraph():
    D = fnx.DiGraph()
    D.add_edge(0, 1)
    D.add_edge(1, 2)
    return D


# ---------------------------------------------------------------------------
# node_link_data / node_link_graph
# ---------------------------------------------------------------------------


class TestNodeLinkFormat:
    def test_round_trip(self, triangle):
        data = fnx.node_link_data(triangle)
        assert "nodes" in data
        assert "edges" in data
        assert len(data["nodes"]) == 3
        assert len(data["edges"]) == 3

        H = fnx.node_link_graph(data)
        assert H.number_of_nodes() == 3
        assert H.number_of_edges() == 3

    def test_with_attrs(self, weighted_graph):
        data = fnx.node_link_data(weighted_graph)
        H = fnx.node_link_graph(data)
        assert H.number_of_edges() == 2

    def test_digraph_round_trip(self, small_digraph):
        data = fnx.node_link_data(small_digraph)
        assert "nodes" in data
        assert "edges" in data
        H = fnx.node_link_graph(data)
        assert H.number_of_nodes() == 3
        assert H.number_of_edges() == 2


# ---------------------------------------------------------------------------
# read/write_edgelist
# ---------------------------------------------------------------------------


class TestEdgelistIO:
    def test_round_trip(self, triangle):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".edgelist", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_edgelist(triangle, path)
            H = fnx.read_edgelist(path)
            assert H.number_of_edges() == 3
        finally:
            os.unlink(path)

    def test_digraph(self, small_digraph):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".edgelist", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_edgelist(small_digraph, path)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_binary_file_like_round_trip(self, triangle):
        buffer = io.BytesIO()
        fnx.write_edgelist(triangle, buffer)
        buffer.seek(0)
        H = fnx.read_edgelist(buffer)
        assert H.number_of_nodes() == 3
        assert H.number_of_edges() == 3


# ---------------------------------------------------------------------------
# read/write_adjlist
# ---------------------------------------------------------------------------


class TestAdjlistIO:
    def test_round_trip(self, triangle):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".adjlist", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_adjlist(triangle, path)
            H = fnx.read_adjlist(path)
            assert H.number_of_nodes() == 3
        finally:
            os.unlink(path)

    def test_digraph_round_trip(self, small_digraph):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".adjlist", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_adjlist(small_digraph, path)
            H = fnx.read_adjlist(path)
            # adjlist doesn't preserve direction; result is undirected Graph
            assert H.number_of_nodes() == 3
        finally:
            os.unlink(path)

    def test_large_graph(self):
        G = fnx.path_graph(100)
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".adjlist", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_adjlist(G, path)
            H = fnx.read_adjlist(path)
            assert H.number_of_nodes() == 100
        finally:
            os.unlink(path)

    def test_binary_file_like_round_trip(self, triangle):
        buffer = io.BytesIO()
        fnx.write_adjlist(triangle, buffer)
        buffer.seek(0)
        H = fnx.read_adjlist(buffer)
        assert H.number_of_nodes() == 3
        assert H.number_of_edges() == 3


# ---------------------------------------------------------------------------
# read/write_graphml
# ---------------------------------------------------------------------------


class TestGraphMLIO:
    def test_round_trip(self, triangle):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".graphml", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_graphml(triangle, path)
            H = fnx.read_graphml(path)
            assert H.number_of_nodes() == 3
            assert H.number_of_edges() == 3
        finally:
            os.unlink(path)

    def test_weighted(self, weighted_graph):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".graphml", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_graphml(weighted_graph, path)
            H = fnx.read_graphml(path)
            assert H.number_of_edges() == 2
            # Weights are preserved as strings in GraphML by default in our implementation
            w1 = H["0"]["1"]["weight"]
            assert float(w1) == 1.5
        finally:
            os.unlink(path)

    def test_directed_graphml(self):
        D = fnx.DiGraph()
        D.add_edge("a", "b")
        D.add_edge("b", "a")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".graphml", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_graphml(D, path)
            H = fnx.read_graphml(path)
            assert isinstance(H, fnx.DiGraph)
            assert H.has_edge("a", "b")
            assert H.has_edge("b", "a")
            assert H.number_of_nodes() == 2
            assert H.number_of_edges() == 2
        finally:
            os.unlink(path)

    def test_node_attrs_preserved(self):
        G = fnx.Graph()
        G.add_node("a", color="red")
        G.add_node("b", color="blue")
        G.add_edge("a", "b")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".graphml", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_graphml(G, path)
            H = fnx.read_graphml(path)
            assert H.nodes["a"]["color"] == "red"
            assert H.nodes["b"]["color"] == "blue"
        finally:
            os.unlink(path)

    def test_edge_attrs_preserved(self):
        G = fnx.Graph()
        G.add_edge("a", "b", weight="1.0", label="edge1")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".graphml", delete=False
        ) as f:
            path = f.name

        try:
            fnx.write_graphml(G, path)
            H = fnx.read_graphml(path)
            data = H.get_edge_data("a", "b")
            assert data["weight"] == "1.0"
            assert data["label"] == "edge1"
        finally:
            os.unlink(path)

    def test_binary_file_like_round_trip(self, triangle):
        buffer = io.BytesIO()
        fnx.write_graphml(triangle, buffer)
        buffer.seek(0)
        H = fnx.read_graphml(buffer)
        assert H.number_of_nodes() == 3
        assert H.number_of_edges() == 3
