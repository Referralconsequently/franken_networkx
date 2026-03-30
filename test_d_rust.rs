use fnx_classes::digraph::DiGraph;

fn main() {
    let g = DiGraph::strict();
    println!("successors missing node: {:?}", g.successors("A"));
}
