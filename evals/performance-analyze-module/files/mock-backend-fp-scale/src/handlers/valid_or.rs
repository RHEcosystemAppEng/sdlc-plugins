// SYNTHETIC TEST DATA — FALSE POSITIVE guard for eval 8
// FALSE POSITIVE 7.6.7: OR across INNER JOINed small reference tables
//
// This handler uses OR conditions spanning an INNER JOINed table (status_code),
// which is a small reference table (~50 rows). INNER JOIN OR conditions are
// handled well by the optimizer. The skill should NOT flag this as Cross-Table OR.

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;

#[get("/api/v2/components/by-status")]
pub async fn find_by_status(
    db: web::Data<DatabaseConnection>,
    query: web::Query<StatusQuery>,
) -> actix_web::Result<impl Responder> {
    let results = component::Entity::find()
        .join(JoinType::InnerJoin, component::Relation::StatusCode.def())
        .filter(
            Condition::any()
                .add(component::Column::Name.contains(&query.q))
                .add(status_code::Column::Label.contains(&query.q))
        )
        .all(db.get_ref())
        .await
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    Ok(HttpResponse::Ok().json(results))
}

#[derive(serde::Deserialize)]
pub struct StatusQuery {
    pub q: String,
}
