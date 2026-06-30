// SYNTHETIC TEST DATA — Minimal handler module for eval

use actix_web::{get, web, HttpResponse};

#[get("/api/v2/licenses")]
async fn list_licenses() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({"licenses": []}))
}

pub fn configure(cfg: &mut web::ServiceConfig) {
    cfg.service(list_licenses);
}
