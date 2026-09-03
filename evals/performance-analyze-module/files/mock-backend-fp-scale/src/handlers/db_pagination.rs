// SYNTHETIC TEST DATA — FALSE POSITIVE guard for eval 8
// FALSE POSITIVE 7.4.1: Pagination flows into SQL .limit().offset()
//
// This handler correctly applies pagination at the database level.
// The .limit() and .offset() calls are on the query itself, not on
// an in-memory collection. The skill should NOT flag this as Late Pagination.

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;

#[get("/api/v2/components/paginated")]
pub async fn list_paginated_components(
    db: web::Data<DatabaseConnection>,
    params: web::Query<PaginationParams>,
) -> actix_web::Result<impl Responder> {
    let total = component::Entity::find()
        .count(db.get_ref())
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // Correct: pagination applied at DB level
    let results = component::Entity::find()
        .limit(params.limit as u64)
        .offset(params.offset as u64)
        .all(db.get_ref())
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    Ok(HttpResponse::Ok().json(serde_json::json!({
        "items": results,
        "total": total,
        "limit": params.limit,
        "offset": params.offset,
    })))
}

#[derive(serde::Deserialize)]
pub struct PaginationParams {
    #[serde(default = "default_limit")]
    pub limit: usize,
    #[serde(default)]
    pub offset: usize,
}

fn default_limit() -> usize { 20 }
