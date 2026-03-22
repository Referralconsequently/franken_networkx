"""Pure-Python graph I/O helpers layered on top of the core bindings."""

from io import BytesIO

from franken_networkx.drawing.layout import _to_nx


def _normalize_lines(lines):
    """Normalize a string or iterable into a list of text lines."""
    if isinstance(lines, str):
        return lines.splitlines()
    return list(lines)


def _empty_like_nx_graph(graph, create_using=None):
    """Build an empty FrankenNetworkX graph matching the NetworkX result shape."""
    import franken_networkx as fnx

    if create_using is None:
        if graph.is_multigraph():
            return fnx.MultiDiGraph() if graph.is_directed() else fnx.MultiGraph()
        return fnx.DiGraph() if graph.is_directed() else fnx.Graph()

    if isinstance(create_using, type):
        return create_using()

    create_using.clear()
    return create_using


def _from_nx_graph(graph, create_using=None):
    """Convert a NetworkX graph into the FrankenNetworkX Python surface."""
    result = _empty_like_nx_graph(graph, create_using=create_using)

    for key, value in graph.graph.items():
        result.graph[key] = value

    for node, attrs in graph.nodes(data=True):
        result.add_node(node, **attrs)

    if graph.is_multigraph():
        for left, right, _, attrs in graph.edges(keys=True, data=True):
            result.add_edge(left, right, **attrs)
    else:
        for left, right, attrs in graph.edges(data=True):
            result.add_edge(left, right, **attrs)

    return result


def parse_adjlist(lines, comments="#", delimiter=None, create_using=None, nodetype=None):
    """Parse an adjacency-list line stream into a FrankenNetworkX graph."""
    import networkx as nx

    graph = nx.parse_adjlist(
        _normalize_lines(lines),
        comments=comments,
        delimiter=delimiter,
        create_using=None,
        nodetype=nodetype,
    )
    return _from_nx_graph(graph, create_using=create_using)


def parse_edgelist(
    lines,
    comments="#",
    delimiter=None,
    create_using=None,
    nodetype=None,
    data=True,
):
    """Parse an edge-list line stream into a FrankenNetworkX graph."""
    import networkx as nx

    graph = nx.parse_edgelist(
        _normalize_lines(lines),
        comments=comments,
        delimiter=delimiter,
        create_using=None,
        nodetype=nodetype,
        data=data,
    )
    return _from_nx_graph(graph, create_using=create_using)


def parse_gml(lines, label="label", destringizer=None):
    """Parse GML text or lines into a FrankenNetworkX graph."""
    import networkx as nx

    graph = nx.parse_gml(_normalize_lines(lines), label=label, destringizer=destringizer)
    return _from_nx_graph(graph)


def generate_adjlist(G, delimiter=" "):
    """Yield adjacency-list lines using NetworkX's generator."""
    import networkx as nx

    yield from nx.generate_adjlist(_to_nx(G), delimiter=delimiter)


def generate_edgelist(G, delimiter=" ", data=True):
    """Yield edge-list lines using NetworkX's generator."""
    import networkx as nx

    yield from nx.generate_edgelist(_to_nx(G), delimiter=delimiter, data=data)


def generate_gml(G, stringizer=None):
    """Yield GML lines using NetworkX's generator."""
    import networkx as nx

    yield from nx.generate_gml(_to_nx(G), stringizer=stringizer)


def write_graphml_xml(
    G,
    path,
    encoding="utf-8",
    prettyprint=True,
    named_key_ids=False,
    edge_id_from_attribute=None,
):
    """Write GraphML through the existing core implementation."""
    import franken_networkx as fnx

    return fnx.write_graphml(G, path)


def write_graphml_lxml(
    G,
    path,
    encoding="utf-8",
    prettyprint=True,
    named_key_ids=False,
    edge_id_from_attribute=None,
):
    """Write GraphML through the existing core implementation."""
    import franken_networkx as fnx

    return fnx.write_graphml(G, path)


def read_gexf(path, node_type=None, relabel=False, version="1.2draft"):
    """Read GEXF through NetworkX and convert the result back to FrankenNetworkX."""
    import networkx as nx

    graph = nx.read_gexf(
        path,
        node_type=node_type,
        relabel=relabel,
        version=version,
    )
    return _from_nx_graph(graph)


def write_gexf(G, path, encoding="utf-8", prettyprint=True, version="1.2draft"):
    """Write GEXF through NetworkX."""
    import networkx as nx

    return nx.write_gexf(
        _to_nx(G),
        path,
        encoding=encoding,
        prettyprint=prettyprint,
        version=version,
    )


def generate_gexf(G, encoding="utf-8", prettyprint=True, version="1.2draft"):
    """Yield GEXF lines through NetworkX."""
    import networkx as nx

    yield from nx.generate_gexf(
        _to_nx(G),
        encoding=encoding,
        prettyprint=prettyprint,
        version=version,
    )


def parse_gexf(string, node_type=None, relabel=False, version="1.2draft"):
    """Parse a GEXF string into a FrankenNetworkX graph."""
    return read_gexf(
        BytesIO(string.encode("utf-8")),
        node_type=node_type,
        relabel=relabel,
        version=version,
    )


def relabel_gexf_graph(G):
    """Relabel a GEXF graph from internal ids to labels via NetworkX."""
    import networkx as nx

    return _from_nx_graph(nx.relabel_gexf_graph(_to_nx(G)))
