# FEATURE_PARITY

## Status Legend

- not_started
- in_progress
- parity_green
- parity_gap

## Porting-to-Rust Phase Status

- phase 4 (implementation from spec): active
- phase 5 (conformance + QA): active

Rule: parity status can move to `parity_green` only with fixture-backed conformance evidence, not implementation completion alone.

## Parity Matrix

| Feature Family | Status | Notes |
|---|---|---|
| Graph/DiGraph/MultiGraph semantics | in_progress | `fnx-classes` now has deterministic undirected graph core, mutation ops, attr merge, evidence ledger hooks. |
| View and mutation contracts | in_progress | `fnx-views` now provides live node/edge/neighbor views plus revision-aware cached snapshots. |
| Dispatchable/backend behavior | in_progress | `fnx-dispatch` now has deterministic backend registry, strict/hardened fail-closed routing, and dispatch evidence ledger. |
| Algorithm core families | in_progress | `fnx-algorithms` now ships unweighted + weighted shortest path, multi-source Dijkstra (`multi_source_dijkstra`), Bellman-Ford shortest paths (`bellman_ford_shortest_paths`), connected-components/component-count, articulation points (`tarjan_articulation_points`), bridges (`tarjan_bridges`), degree-centrality, closeness-centrality, harmonic-centrality, Katz-centrality, HITS centrality (hubs + authorities), PageRank, eigenvector-centrality, betweenness-centrality, edge-betweenness-centrality, clustering coefficient (`clustering_coefficient` with `average_clustering` and `transitivity`), deterministic maximal matching (`greedy_maximal_matching`), matching validation APIs (`is_matching`, `is_maximal_matching`, `is_perfect_matching`), blossom-optimal weighted matching (`blossom_max_weight_matching`, `blossom_min_weight_matching`), deterministic max-flow (`edmonds_karp_max_flow`), deterministic minimum-cut (`edmonds_karp_minimum_cut`), minimum s-t edge cut (`edmonds_karp_minimum_st_edge_cut`), pair/global edge connectivity (`edmonds_karp_edge_connectivity`, `edmonds_karp_global_edge_connectivity`), and global minimum edge cut (`edmonds_karp_global_minimum_edge_cut`), distance measures (`distance_measures` computing eccentricity, diameter, radius, center, periphery), average shortest path length (`average_shortest_path_length`), connectivity check (`is_connected`), graph density (`density`), path existence (`has_path`), single-pair shortest path length (`shortest_path_length`), minimum spanning tree (`minimum_spanning_tree` via Kruskal), triangle counting (`triangles`), square clustering (`square_clustering`), tree/forest detection (`is_tree`, `is_forest`), greedy graph coloring (`greedy_color`), bipartite detection (`is_bipartite`, `bipartite_sets`), k-core decomposition (`core_number`), average neighbor degree (`average_neighbor_degree`), degree assortativity (`degree_assortativity_coefficient`), VoteRank (`voterank`), clique enumeration (`find_cliques`, `graph_clique_number` via Bron-Kerbosch with pivoting), node connectivity (`node_connectivity`, `global_node_connectivity`) and minimum node cut (`minimum_node_cut`, `global_minimum_node_cut` via node-splitting Edmonds-Karp), cycle basis (`cycle_basis` via Paton's algorithm), all simple paths enumeration (`all_simple_paths`), global/local efficiency metrics (`global_efficiency`, `local_efficiency`), minimum edge cover (`min_edge_cover`), and Euler path/circuit algorithms (`is_eulerian`, `has_eulerian_path`, `is_semieulerian`, `eulerian_circuit`, `eulerian_path` via Hierholzer's algorithm) with complexity witnesses; additional centrality/flow families and remaining weighted shortest-path APIs remain pending. |
| Graph generator families | in_progress | `fnx-generators` now ships deterministic `empty/path/star/cycle/complete` and seeded `gnp_random_graph` with strict/hardened parameter controls. |
| Conversion baseline behavior | in_progress | `fnx-convert` ships edge-list/adjacency conversions with strict/hardened malformed-input handling and normalization output. |
| Read/write baseline formats | in_progress | `fnx-readwrite` ships deterministic edgelist + adjacency-list + JSON graph parse/write with strict/hardened parser modes. |
| Differential conformance harness | in_progress | `fnx-conformance` executes graph + views + dispatch + convert + readwrite + components + generators + centrality + clustering + flow + structure (articulation points, bridges) + matching (maximal, max-weight, min-weight) + Bellman-Ford + multi-source Dijkstra + GNP random graph + distance measures + average shortest path length + is_connected + density + has_path + shortest_path_length + minimum spanning tree (Kruskal) + triangles + square clustering + tree/forest detection + greedy coloring + bipartite detection + k-core decomposition + average neighbor degree + degree assortativity + VoteRank + clique enumeration + node connectivity + cycle basis + all simple paths + global/local efficiency + minimum edge cover + Euler path/circuit fixtures and emits report artifacts under `artifacts/conformance/latest/` (currently 59 fixtures across 12 E2E journeys). |
| RaptorQ durability pipeline | in_progress | `fnx-durability` generates RaptorQ sidecars, runs scrub verification, and emits decode proofs for conformance reports. |
| Benchmark percentile gating | in_progress | `scripts/run_benchmark_gate.sh` emits p50/p95/p99 artifact and enforces threshold budgets with durability sidecars. |

## Required Evidence Per Feature Family

1. Differential fixture report.
2. Edge-case/adversarial test results.
3. Benchmark delta (when performance-sensitive).
4. Documented compatibility exceptions (if any).

## Conformance Gate Checklist (Phase 5)

All CPU-heavy checks must be offloaded using `rch`.

```bash
rch exec -- cargo test -p fnx-conformance --test smoke -- --nocapture
rch exec -- cargo test -p fnx-conformance --test phase2c_packet_readiness_gate -- --nocapture
rch exec -- cargo test --workspace
rch exec -- cargo clippy --workspace --all-targets -- -D warnings
rch exec -- cargo fmt --check
```

Parity release condition:

1. no strict-mode drift on scoped fixtures.
2. hardened divergences explicitly allowlisted and evidence-linked.
3. replay metadata and forensics links present in structured logs.
4. durability artifacts (sidecar/scrub/decode-proof) verified for long-lived evidence sets.
