"""NetworkX backend dispatch interface.

When installed alongside NetworkX 3.0+, FrankenNetworkX can accelerate
supported algorithms transparently via the backend dispatch protocol.

Usage::

    import networkx as nx
    nx.config.backend_priority = ["franken_networkx"]
    # All supported algorithms now dispatch to Rust.
"""
