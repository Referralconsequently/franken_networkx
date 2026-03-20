import franken_networkx as fnx
g = fnx.DiGraph()
g.add_edge("a", "b", weight=1.0)
g.add_edge("b", "c", weight=2.0)
print("nodes:", g.nodes)
print("edges:", g.edges)
print(fnx.multi_source_dijkstra(g, ["b"], weight="weight"))
print(fnx.single_source_dijkstra(g, "b", weight="weight"))
