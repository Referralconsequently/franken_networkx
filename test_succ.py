import franken_networkx as fnx
g = fnx.DiGraph()
g.add_edge("a", "b", weight=1.0)
g.add_edge("b", "c", weight=2.0)
print(g.successors("b"))
print(g.predecessors("b"))
