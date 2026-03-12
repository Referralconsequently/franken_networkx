"""Tests for additional DAG algorithm bindings.

Tests cover:
- is_aperiodic
- antichains
- immediate_dominators
- dominance_frontiers
"""

import pytest
import franken_networkx as fnx


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def chain():
    """a->b->c."""
    g = fnx.DiGraph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    return g


@pytest.fixture
def diamond():
    """a->b, a->c, b->d, c->d."""
    g = fnx.DiGraph()
    g.add_edge("a", "b")
    g.add_edge("a", "c")
    g.add_edge("b", "d")
    g.add_edge("c", "d")
    return g


@pytest.fixture
def cycle3():
    """a->b->c->a."""
    g = fnx.DiGraph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    return g


# ---------------------------------------------------------------------------
# is_aperiodic
# ---------------------------------------------------------------------------

class TestIsAperiodic:
    def test_cycle_periodic(self, cycle3):
        assert fnx.is_aperiodic(cycle3) is False

    def test_with_self_loop(self):
        g = fnx.DiGraph()
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        g.add_edge("c", "a")
        g.add_edge("a", "a")
        assert fnx.is_aperiodic(g) is True

    def test_two_cycle_lengths(self):
        g = fnx.DiGraph()
        g.add_edge("a", "b")
        g.add_edge("b", "a")
        g.add_edge("a", "c")
        g.add_edge("c", "d")
        g.add_edge("d", "a")
        assert fnx.is_aperiodic(g) is True

    def test_dag_is_aperiodic(self, chain):
        # DAGs have no cycles, trivially aperiodic
        assert fnx.is_aperiodic(chain) is True

    def test_raises_on_undirected(self):
        g = fnx.Graph()
        g.add_edge("a", "b")
        with pytest.raises(fnx.NetworkXNotImplemented):
            fnx.is_aperiodic(g)


# ---------------------------------------------------------------------------
# antichains
# ---------------------------------------------------------------------------

class TestAntichains:
    def test_chain(self, chain):
        acs = fnx.antichains(chain)
        # Chain a->b->c: antichains are {}, {a}, {b}, {c}
        assert len(acs) == 4
        assert [] in acs

    def test_diamond(self, diamond):
        acs = fnx.antichains(diamond)
        # b and c are incomparable
        has_bc = any(
            set(ac) == {"b", "c"} for ac in acs
        )
        assert has_bc

    def test_empty(self):
        g = fnx.DiGraph()
        acs = fnx.antichains(g)
        assert acs == [[]]

    def test_raises_on_undirected(self):
        g = fnx.Graph()
        g.add_edge("a", "b")
        with pytest.raises(fnx.NetworkXNotImplemented):
            fnx.antichains(g)


# ---------------------------------------------------------------------------
# immediate_dominators
# ---------------------------------------------------------------------------

class TestImmediateDominators:
    def test_chain(self, chain):
        idom = fnx.immediate_dominators(chain, "a")
        assert idom["a"] == "a"
        assert idom["b"] == "a"
        assert idom["c"] == "b"

    def test_diamond(self, diamond):
        idom = fnx.immediate_dominators(diamond, "a")
        assert idom["a"] == "a"
        assert idom["b"] == "a"
        assert idom["c"] == "a"
        assert idom["d"] == "a"

    def test_raises_on_undirected(self):
        g = fnx.Graph()
        g.add_edge("a", "b")
        with pytest.raises(fnx.NetworkXNotImplemented):
            fnx.immediate_dominators(g, "a")


# ---------------------------------------------------------------------------
# dominance_frontiers
# ---------------------------------------------------------------------------

class TestDominanceFrontiers:
    def test_chain(self, chain):
        df = fnx.dominance_frontiers(chain, "a")
        # No join points in a chain
        assert all(len(v) == 0 for v in df.values())

    def test_diamond(self, diamond):
        df = fnx.dominance_frontiers(diamond, "a")
        assert "d" in df["b"]
        assert "d" in df["c"]
        assert len(df["a"]) == 0

    def test_raises_on_undirected(self):
        g = fnx.Graph()
        g.add_edge("a", "b")
        with pytest.raises(fnx.NetworkXNotImplemented):
            fnx.dominance_frontiers(g, "a")
