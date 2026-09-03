// SYNTHETIC TEST DATA — Backend handlers with GET + POST endpoints for tracing eval
use actix_web::{web, HttpResponse};

#[get("/api/v2/packages")]
pub async fn list_packages() -> HttpResponse {
    HttpResponse::Ok().json(vec!["pkg-1", "pkg-2", "pkg-3"])
}

#[get("/api/v2/packages/{id}")]
pub async fn get_package(path: web::Path<String>) -> HttpResponse {
    let id = path.into_inner();
    HttpResponse::Ok().json(format!("Package {}", id))
}

#[post("/api/v2/packages/{id}/vulnerabilities")]
pub async fn scan_vulnerabilities(path: web::Path<String>) -> HttpResponse {
    HttpResponse::Ok().json("scan started")
}
