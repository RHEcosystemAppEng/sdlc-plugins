// SYNTHETIC TEST DATA — FALSE POSITIVE guard for eval 8
// FALSE POSITIVE 7.6.8: Load all nodes → build petgraph → BFS traversal
//
// This handler loads all nodes for an SBOM, builds a petgraph dependency
// graph, and performs BFS traversal to find all transitive dependencies.
// The graph traversal IS the primary output — it cannot be expressed as
// a SQL WHERE clause. The skill should Discard this finding via the
// graph traversal false-positive guard.

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;
use petgraph::Graph;
use petgraph::algo::dijkstra;
use uuid::Uuid;
use std::collections::HashMap;

#[get("/api/v2/sbom/{id}/dependencies")]
pub async fn get_transitive_dependencies(
    db: web::Data<DatabaseConnection>,
    path: web::Path<Uuid>,
) -> actix_web::Result<impl Responder> {
    let sbom_id = path.into_inner();

    // Load all nodes for this SBOM
    let nodes = sbom_node::Entity::find()
        .filter(sbom_node::Column::SbomId.eq(sbom_id))
        .all(db.get_ref())
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // Load all edges
    let edges = package_relates_to_package::Entity::find()
        .filter(package_relates_to_package::Column::SbomId.eq(sbom_id))
        .all(db.get_ref())
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // Build petgraph — graph traversal requires full structure
    let mut graph = Graph::new();
    let mut node_indices = HashMap::new();

    for node in &nodes {
        let idx = graph.add_node(node.node_id.clone());
        node_indices.insert(node.node_id.clone(), idx);
    }

    for edge in &edges {
        if let (Some(&from), Some(&to)) = (
            node_indices.get(&edge.left_node_id),
            node_indices.get(&edge.right_node_id),
        ) {
            graph.add_edge(from, to, edge.relationship.clone());
        }
    }

    // BFS/Dijkstra traversal — this IS the output, not a search filter
    let root = node_indices.values().next().unwrap();
    let distances = dijkstra(&graph, *root, None, |_| 1);

    let dependency_count = distances.len();
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "sbom_id": sbom_id,
        "total_dependencies": dependency_count,
    })))
}
