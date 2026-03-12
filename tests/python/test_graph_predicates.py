"""Tests for graph predicate algorithm bindings.

Tests cover:
- is_graphical, is_digraphical, is_multigraphical, is_pseudographical
- is_regular, is_k_regular
- is_tournament
- is_weighted, is_negatively_weighted
- is_path
- is_distance_regular
"""

import pytest
import franken_networkx as fnx


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def triangle():
    g = fnx.Graph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    return g


@pytest.fixture
def path3():
    """Path a-b-c."""
    g = fnx.Graph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    return g


# ---------------------------------------------------------------------------
# Degree sequence predicates
# ---------------------------------------------------------------------------

class TestIsGraphical:
    def test_triangle(self):
        assert fnx.is_graphical([2, 2, 2]) is True

    def test_single_edge(self):
        assert fnx.is_graphical([1, 1]) is True

    def test_empty(self):
        assert fnx.is_graphical([]) is True

    def test_odd_sum(self):
        assert fnx.is_graphical([1]) is False

    def test_degree_too_high(self):
        assert fnx.is_graphical([3, 1, 1]) is False

    def test_star(self):
        assert fnx.is_graphical([3, 1, 1, 1]) is True


class TestIsDigraphical:
    def test_mutual(self):
        assert fnx.is_digraphical([(1, 1), (1, 1)]) is True

    def test_one_way(self):
        assert fnx.is_digraphical([(1, 0), (0, 1)]) is True

    def test_empty(self):
        assert fnx.is_digraphical([]) is True

    def test_unbalanced(self):
        assert fnx.is_digraphical([(2, 0), (0, 1)]) is False


class TestIsMultigraphical:
    def test_valid(self):
        assert fnx.is_multigraphical([2, 2, 2]) is True

    def test_high_degree(self):
        assert fnx.is_multigraphical([4, 2, 2]) is True

    def test_odd_sum(self):
        assert fnx.is_multigraphical([1]) is False


class TestIsPseudographical:
    def test_self_loop(self):
        assert fnx.is_pseudographical([2]) is True

    def test_odd_sum(self):
        assert fnx.is_pseudographical([1]) is False


# ---------------------------------------------------------------------------
# Graph regularity
# ---------------------------------------------------------------------------

class TestIsRegular:
    def test_triangle(self, triangle):
        assert fnx.is_regular(triangle) is True

    def test_path(self, path3):
        assert fnx.is_regular(path3) is False

    def test_single_node(self):
        g = fnx.Graph()
        g.add_node("a")
        assert fnx.is_regular(g) is True


class TestIsKRegular:
    def test_triangle_2regular(self, triangle):
        assert fnx.is_k_regular(triangle, 2) is True
        assert fnx.is_k_regular(triangle, 1) is False

    def test_empty_0regular(self):
        g = fnx.Graph()
        g.add_node("a")
        g.add_node("b")
        assert fnx.is_k_regular(g, 0) is True


# ---------------------------------------------------------------------------
# Tournament
# ---------------------------------------------------------------------------

class TestIsTournament:
    def test_complete_oriented(self):
        g = fnx.DiGraph()
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        g.add_edge("a", "c")
        assert fnx.is_tournament(g) is True

    def test_missing_edge(self):
        g = fnx.DiGraph()
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        assert fnx.is_tournament(g) is False

    def test_raises_on_undirected(self, triangle):
        with pytest.raises(fnx.NetworkXNotImplemented):
            fnx.is_tournament(triangle)


# ---------------------------------------------------------------------------
# Weighted predicates
# ---------------------------------------------------------------------------

class TestIsWeighted:
    def test_weighted(self):
        g = fnx.Graph()
        g.add_edge("a", "b", weight=1.0)
        assert fnx.is_weighted(g) is True

    def test_not_weighted(self, path3):
        assert fnx.is_weighted(path3) is False

    def test_custom_attr(self):
        g = fnx.Graph()
        g.add_edge("a", "b", cost=5.0)
        assert fnx.is_weighted(g, weight="cost") is True
        assert fnx.is_weighted(g) is False


class TestIsNegativelyWeighted:
    def test_negative(self):
        g = fnx.Graph()
        g.add_edge("a", "b", weight=-1.0)
        assert fnx.is_negatively_weighted(g) is True

    def test_positive(self):
        g = fnx.Graph()
        g.add_edge("a", "b", weight=1.0)
        assert fnx.is_negatively_weighted(g) is False


# ---------------------------------------------------------------------------
# Path graph
# ---------------------------------------------------------------------------

class TestIsPath:
    def test_path(self, path3):
        assert fnx.is_path(path3) is True

    def test_cycle_not_path(self, triangle):
        assert fnx.is_path(triangle) is False

    def test_single_node(self):
        g = fnx.Graph()
        g.add_node("a")
        assert fnx.is_path(g) is True


# ---------------------------------------------------------------------------
# Distance-regular
# ---------------------------------------------------------------------------

class TestIsDistanceRegular:
    def test_cycle_5(self):
        g = fnx.Graph()
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        g.add_edge("c", "d")
        g.add_edge("d", "e")
        g.add_edge("e", "a")
        assert fnx.is_distance_regular(g) is True

    def test_path_not_regular(self):
        g = fnx.Graph()
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        g.add_edge("c", "d")
        assert fnx.is_distance_regular(g) is False

    def test_complete_graph(self, triangle):
        assert fnx.is_distance_regular(triangle) is True
