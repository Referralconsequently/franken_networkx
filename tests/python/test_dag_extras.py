"""Tests for DAG extra functions: dag_longest_path, dag_longest_path_length,
lexicographic_topological_sort, topological_generations."""

import pytest

import franken_networkx as fnx


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def diamond_dag():
    """DAG: 0->1, 0->2, 1->3, 2->3."""
    D = fnx.DiGraph()
    D.add_edge(0, 1)
    D.add_edge(0, 2)
    D.add_edge(1, 3)
    D.add_edge(2, 3)
    return D


@pytest.fixture
def chain_dag():
    """Linear DAG: 0->1->2->3->4."""
    D = fnx.DiGraph()
    for i in range(4):
        D.add_edge(i, i + 1)
    return D


@pytest.fixture
def wide_dag():
    """Wide DAG: 0->1, 0->2, 0->3, 1->4, 2->4, 3->4."""
    D = fnx.DiGraph()
    D.add_edge(0, 1)
    D.add_edge(0, 2)
    D.add_edge(0, 3)
    D.add_edge(1, 4)
    D.add_edge(2, 4)
    D.add_edge(3, 4)
    return D


# ---------------------------------------------------------------------------
# dag_longest_path
# ---------------------------------------------------------------------------


class TestDagLongestPath:
    def test_chain(self, chain_dag):
        path = fnx.dag_longest_path(chain_dag)
        assert path == [0, 1, 2, 3, 4]

    def test_diamond(self, diamond_dag):
        path = fnx.dag_longest_path(diamond_dag)
        assert len(path) == 3
        assert path[0] == 0
        assert path[-1] == 3

    def test_single_node(self):
        D = fnx.DiGraph()
        D.add_node(0)
        path = fnx.dag_longest_path(D)
        assert path == [0]

    def test_two_nodes(self):
        D = fnx.DiGraph()
        D.add_edge(0, 1)
        path = fnx.dag_longest_path(D)
        assert path == [0, 1]


# ---------------------------------------------------------------------------
# dag_longest_path_length
# ---------------------------------------------------------------------------


class TestDagLongestPathLength:
    def test_chain(self, chain_dag):
        length = fnx.dag_longest_path_length(chain_dag)
        assert length == 4

    def test_diamond(self, diamond_dag):
        length = fnx.dag_longest_path_length(diamond_dag)
        assert length == 2

    def test_single_node(self):
        D = fnx.DiGraph()
        D.add_node(0)
        length = fnx.dag_longest_path_length(D)
        assert length == 0

    def test_wide(self, wide_dag):
        length = fnx.dag_longest_path_length(wide_dag)
        assert length == 2


# ---------------------------------------------------------------------------
# lexicographic_topological_sort
# ---------------------------------------------------------------------------


class TestLexicographicTopologicalSort:
    def test_diamond(self, diamond_dag):
        order = list(fnx.lexicographic_topological_sort(diamond_dag))
        assert set(order) == {0, 1, 2, 3}
        # Must be a valid topological order
        assert order.index(0) < order.index(1)
        assert order.index(0) < order.index(2)
        assert order.index(1) < order.index(3)
        assert order.index(2) < order.index(3)

    def test_lexicographic_tiebreak(self):
        """When multiple sources exist, smaller label should come first."""
        D = fnx.DiGraph()
        D.add_edge(0, 2)
        D.add_edge(1, 2)
        order = list(fnx.lexicographic_topological_sort(D))
        # Both 0 and 1 are sources; lexicographic means 0 before 1
        assert order.index(0) < order.index(1)

    def test_chain(self, chain_dag):
        order = list(fnx.lexicographic_topological_sort(chain_dag))
        assert order == [0, 1, 2, 3, 4]

    def test_cycle_raises(self):
        D = fnx.DiGraph()
        D.add_edge(0, 1)
        D.add_edge(1, 0)
        with pytest.raises(fnx.HasACycle):
            list(fnx.lexicographic_topological_sort(D))


# ---------------------------------------------------------------------------
# topological_generations
# ---------------------------------------------------------------------------


class TestTopologicalGenerations:
    def test_diamond(self, diamond_dag):
        gens = list(fnx.topological_generations(diamond_dag))
        assert len(gens) == 3
        assert set(gens[0]) == {0}
        assert set(gens[1]) == {1, 2}
        assert set(gens[2]) == {3}

    def test_chain(self, chain_dag):
        gens = list(fnx.topological_generations(chain_dag))
        assert len(gens) == 5
        for i, gen in enumerate(gens):
            assert gen == [i]

    def test_wide(self, wide_dag):
        gens = list(fnx.topological_generations(wide_dag))
        assert len(gens) == 3
        assert set(gens[0]) == {0}
        assert set(gens[1]) == {1, 2, 3}
        assert set(gens[2]) == {4}

    def test_single_node(self):
        D = fnx.DiGraph()
        D.add_node(42)
        gens = list(fnx.topological_generations(D))
        assert len(gens) == 1
        assert gens[0] == [42]

    def test_cycle_raises(self):
        D = fnx.DiGraph()
        D.add_edge(0, 1)
        D.add_edge(1, 0)
        with pytest.raises(fnx.HasACycle):
            list(fnx.topological_generations(D))
