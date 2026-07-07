# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose
Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Full File Content

```rust
use actix_web::HttpResponse;
use axum::{
    extract::{Path, State},
    Json,
};
use uuid::Uuid;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use crate::AppState;
use trustify_common::error::AppError;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated advisory severity counts for the given SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Uuid, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn get_severity_summary(
    Path(id): Path<Uuid>,
    State(state): State<AppState>,
) -> Result<Json<SeveritySummary>, AppError> {
    let db = state.db();
    let service = AdvisoryService::new(db.clone());

    let summary = service
        .severity_summary(id, &db)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {id} not found")))?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Handler pattern**: Follows the exact pattern from `advisory/endpoints/get.rs` — extract path param and state, call service, map None to 404, return Json.
- **utoipa annotation**: Includes OpenAPI documentation via the `#[utoipa::path]` macro, matching how other endpoints document their routes for Swagger UI generation.
- **Error message**: The 404 message includes the SBOM ID for debuggability, following the pattern in sibling handlers.
- **Service construction**: `AdvisoryService::new(db.clone())` or `state.advisory_service()` depending on how the service is obtained in sibling code — will be adjusted during implementation to match the exact pattern used.
- **No pagination**: This endpoint returns a single summary object, not a list, so no `PaginatedResults` wrapper is needed.
