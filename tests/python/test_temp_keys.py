import networkx as nx

G = nx.MultiGraph()
G.add_edge("a", "b", key=5)
print("k1:", G.add_edge("a", "b")) # NetworkX returns 1. Wait, length is 1, so key=1
print("k2:", G.add_edge("a", "b", key=1)) # Overwrites key 1 or creates? Wait, key 1 already exists, so overwrites.
print("k3:", G.add_edge("a", "b")) # Keys are 5, 1. length is 2. So key=2.

G2 = nx.MultiGraph()
G2.add_edge("a", "b", key=5)
G2.add_edge("a", "b", key=0)
print("k4:", G2.add_edge("a", "b")) # Length is 2. Keys 5, 0. Tries 2. Returns 2.
