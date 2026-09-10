// SYNTHETIC TEST DATA — Backend handler with planted anti-patterns for eval
// PLANTED ANTI-PATTERN: Step 7.3.2 — Unbounded Query-Driving Iteration
// PLANTED ANTI-PATTERN: Step 7.4.1 — Late Pagination
//
// This handler has two issues:
// 1. It loads an unbounded result set from the database (no LIMIT, no size guard)
//    and iterates each item, executing a DB query per item.
// 2. Pagination parameters exist at the API layer but are applied via
//    paginate_array() AFTER loading all results into memory.

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;
use uuid::Uuid;

use crate::models::{ComponentModel, PaginatedResults, paginate_array};

#[get("/api/v2/components")]
pub async fn list_components_with_details(
    db: web::Data<DatabaseConnection>,
    paginated: web::Query<PaginatedParams>,
) -> actix_web::Result<impl Responder> {
    // No LIMIT on this query — loads all matching components
    let all_components = component::Entity::find()
        .filter(component::Column::Active.eq(true))
        .all(db.get_ref())
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // PLANTED: Unbounded iteration — no .take(N) or size guard
    // Each iteration triggers a DB query to fetch related data
    let mut enriched = Vec::new();
    for component in &all_components {
        let details = component_detail::Entity::find_by_id(component.id)
            .one(db.get_ref())
            .await
            .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

        let vendors = vendor::Entity::find()
            .filter(vendor::Column::ComponentId.eq(component.id))
            .all(db.get_ref())
            .await
            .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

        enriched.push(EnrichedComponent {
            component: component.clone(),
            details,
            vendors,
        });
    }

    // PLANTED: Late pagination — applied AFTER loading all results
    let result = paginate_array(&enriched, paginated.offset, paginated.limit);

    Ok(HttpResponse::Ok().json(result))
}

#[derive(serde::Deserialize)]
pub struct PaginatedParams {
    #[serde(default)]
    pub offset: usize,
    #[serde(default = "default_limit")]
    pub limit: usize,
}

fn default_limit() -> usize { 20 }

#[derive(serde::Serialize, Clone)]
pub struct EnrichedComponent {
    pub component: ComponentModel,
    pub details: Option<component_detail::Model>,
    pub vendors: Vec<vendor::Model>,
}
