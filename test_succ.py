import franken_networkx as fnx

GF = fnx.DiGraph()
GF.add_node("A")
print("FNX has_node:", GF.has_node("A"))
print("FNX out_degree:", GF.out_degree("A"))
try:
    print("FNX successors:", list(GF.successors("A")))
except Exception as e:
    print("FNX successors error:", e)
