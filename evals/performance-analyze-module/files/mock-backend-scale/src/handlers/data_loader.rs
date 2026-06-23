// SYNTHETIC TEST DATA — Backend handler with planted anti-patterns for eval
// PLANTED ANTI-PATTERN: Step 7.6.8 — Load-All-Then-Search
//
// This handler loads ALL items for a category from the database, then
// searches the in-memory collection for items matching the user's search
// term. The search term is known before the query and could be added as
// a WHERE clause, but instead the code loads everything and filters in
// memory. This is NOT a graph traversal case — it's a simple linear search.

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;
use uuid::Uuid;

use crate::models::ComponentModel;

#[get("/api/v2/categories/{category_id}/components")]
pub async fn search_components_in_category(
    db: web::Data<DatabaseConnection>,
    path: web::Path<Uuid>,
    query: web::Query<SearchParams>,
) -> actix_web::Result<impl Responder> {
    let category_id = path.into_inner();
    let search_term = &query.name;

    // Load ALL components for this category — no search filter in query
    let all_components = component::Entity::find()
        .filter(component::Column::CategoryId.eq(category_id))
        .all(db.get_ref())
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // Search in memory — search_term was available before the query!
    let matching: Vec<_> = all_components
        .iter()
        .filter(|c| c.name.contains(search_term))
        .cloned()
        .collect();

    Ok(HttpResponse::Ok().json(matching))
}

#[derive(serde::Deserialize)]
pub struct SearchParams {
    pub name: String,
}
