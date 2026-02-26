"""Smoke test: verify the package imports and version is accessible."""


def test_import_version():
    import franken_networkx as fnx
    assert fnx.__version__ == "0.1.0"
