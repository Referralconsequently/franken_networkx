"""Tests for additional traversal algorithm bindings.

Tests cover:
- edge_bfs
- edge_dfs
"""

import pytest
import franken_networkx as fnx


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def path3():
    g = fnx.Graph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    return g


@pytest.fixture
def triangle():
    g = fnx.Graph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    return g


@pytest.fixture
def directed_chain():
    g = fnx.DiGraph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    return g


# ---------------------------------------------------------------------------
# edge_bfs
# ---------------------------------------------------------------------------

class TestEdgeBfs:
    def test_path(self, path3):
        edges = fnx.edge_bfs(path3, "a")
        edge_set = {(u, v) for u, v in edges}
        assert ("a", "b") in edge_set
        assert ("b", "c") in edge_set

    def test_directed(self, directed_chain):
        edges = fnx.edge_bfs(directed_chain, "a")
        edge_set = {(u, v) for u, v in edges}
        assert ("a", "b") in edge_set
        assert ("b", "c") in edge_set

    def test_single_node(self):
        g = fnx.Graph()
        g.add_node("a")
        edges = fnx.edge_bfs(g, "a")
        assert edges == []


# ---------------------------------------------------------------------------
# edge_dfs
# ---------------------------------------------------------------------------

class TestEdgeDfs:
    def test_path(self, path3):
        edges = fnx.edge_dfs(path3, "a")
        assert len(edges) >= 2

    def test_directed(self, directed_chain):
        edges = fnx.edge_dfs(directed_chain, "a")
        edge_set = {(u, v) for u, v in edges}
        assert ("a", "b") in edge_set
        assert ("b", "c") in edge_set

    def test_triangle(self, triangle):
        edges = fnx.edge_dfs(triangle, "a")
        # Triangle has 3 edges
        assert len(edges) == 3

    def test_single_node(self):
        g = fnx.Graph()
        g.add_node("a")
        edges = fnx.edge_dfs(g, "a")
        assert edges == []
