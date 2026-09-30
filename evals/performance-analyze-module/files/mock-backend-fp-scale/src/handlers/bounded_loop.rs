// SYNTHETIC TEST DATA — FALSE POSITIVE guard for eval 8
// FALSE POSITIVE 7.3.2: Loop with .take(100) guard — NOT unbounded
//
// This handler iterates query results but limits the iteration to 100 items
// via .take(). The skill should recognize this as a bounded loop and
// NOT flag it as Unbounded Query-Driving Iteration.

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;
use uuid::Uuid;

#[get("/api/v2/components/enriched")]
pub async fn list_enriched_components(
    db: web::Data<DatabaseConnection>,
) -> actix_web::Result<impl Responder> {
    let components = component::Entity::find()
        .all(db.get_ref())
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // Bounded: .take(100) limits iteration
    let mut enriched = Vec::new();
    for component in components.iter().take(100) {
        let detail = component_detail::Entity::find_by_id(component.id)
            .one(db.get_ref())
            .await
            .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

        enriched.push(serde_json::json!({
            "id": component.id,
            "name": component.name,
            "detail": detail,
        }));
    }

    Ok(HttpResponse::Ok().json(enriched))
}
