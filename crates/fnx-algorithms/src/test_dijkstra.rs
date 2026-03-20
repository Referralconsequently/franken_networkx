use fnx_classes::digraph::DiGraph;

#[test]
fn test_directed_multi() {
    let mut g = DiGraph::strict();
    g.add_edge("a", "b").unwrap();
    g.add_edge("b", "c").unwrap();
    println!("successors of b: {:?}", g.successors("b"));
    let res = crate::multi_source_dijkstra_directed(&g, &["b"], "weight");
    println!("dists: {:?}", res.distances);
    assert!(false); // to see the output
}
