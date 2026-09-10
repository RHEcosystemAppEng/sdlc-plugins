// SYNTHETIC TEST DATA — Backend handler with planted anti-patterns for eval
// PLANTED ANTI-PATTERN: Step 7.6.2 enhancement — Chain Depth Auto-Extension
//
// This handler delegates through 4 levels of pure delegation before reaching
// the actual DB query. With chain_depth=3, the skill would stop at level 3
// and miss the query. The auto-extension rule should detect that each
// intermediate function is a pure delegation (single call, returns result)
// and extend the depth to reach the actual query at level 4.
//
// Call chain:
//   get_component_graph (handler, depth 0)
//     → service.load_graphs(conn, ids) (depth 1)
//       → self.inner.load_graphs(conn, ids) (depth 2, pure delegation)
//         → self.load_graphs_inner(conn, ids) (depth 3 = DEFAULT LIMIT, pure delegation)
//           → self.perform_load(conn, id) (depth 4, ACTUAL QUERY — only reachable with auto-extension)

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;
use uuid::Uuid;

pub struct GraphService {
    inner: InnerGraphService,
}

impl GraphService {
    pub async fn load_graphs(&self, conn: &DatabaseConnection, ids: Vec<Uuid>) -> Result<Vec<GraphData>, DbErr> {
        self.inner.load_graphs(conn, ids).await
    }
}

pub struct InnerGraphService;

impl InnerGraphService {
    pub async fn load_graphs(&self, conn: &DatabaseConnection, ids: Vec<Uuid>) -> Result<Vec<GraphData>, DbErr> {
        self.load_graphs_inner(conn, ids).await
    }

    async fn load_graphs_inner(&self, conn: &DatabaseConnection, ids: Vec<Uuid>) -> Result<Vec<GraphData>, DbErr> {
        let mut results = Vec::new();
        for id in ids {
            results.push(self.perform_load(conn, id).await?);
        }
        Ok(results)
    }

    async fn perform_load(&self, conn: &DatabaseConnection, id: Uuid) -> Result<GraphData, DbErr> {
        let nodes = sbom_node::Entity::find()
            .filter(sbom_node::Column::SbomId.eq(id))
            .all(conn)
            .await?;

        let edges = package_relates_to_package::Entity::find()
            .filter(package_relates_to_package::Column::SbomId.eq(id))
            .all(conn)
            .await?;

        Ok(GraphData { nodes, edges })
    }
}

pub struct GraphData {
    pub nodes: Vec<sbom_node::Model>,
    pub edges: Vec<package_relates_to_package::Model>,
}

#[get("/api/v2/analysis/graph/{id}")]
pub async fn get_component_graph(
    service: web::Data<GraphService>,
    db: web::Data<DatabaseConnection>,
    path: web::Path<Uuid>,
) -> actix_web::Result<impl Responder> {
    let id = path.into_inner();
    let graphs = service.load_graphs(db.get_ref(), vec![id])
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    Ok(HttpResponse::Ok().json(graphs.len()))
}
