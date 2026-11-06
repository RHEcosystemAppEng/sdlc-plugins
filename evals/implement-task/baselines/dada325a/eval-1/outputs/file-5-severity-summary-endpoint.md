# File 5 (CREATE): `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose
The GET handler for `/api/v2/sbom/{id}/advisory-summary`. It follows `advisory/endpoints/get.rs`: extract
`Path<Id>`, call the service, return JSON.

## Content
```rust
use axum::{extract::{Path, State}, Json};
use trustify_common::{db::Transactional, error::AppError, id::Id};

use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};

/// Returns counts of unique advisories per severity level for the given SBOM.
///
/// Responds `404 Not Found` when the SBOM does not exist, which matches `GET /api/v2/sbom/{id}`.
#[utoipa::path(
    get,
    tag = "advisory",
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(("id" = Id, Path, description = "SBOM identifier")),
    responses(
        (status = 200, description = "Severity counts for the SBOM", body = SeveritySummary),
        (status = 404, description = "The SBOM could not be found"),
    ),
)]
pub async fn get(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("failed to compute advisory severity summary")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {id} not found")))?;

    Ok(Json(summary))
}
```

## Notes
- The service-extraction style (`State<AdvisoryService>` or an `Extension`) and the exact `AppError::NotFound`
  variant/constructor are copied verbatim from `get.rs` and `common/src/error.rs`.
- `#[utoipa::path]` is included only if `get.rs` uses it. If it is, the handler is also added to the module's
  OpenAPI `paths(...)` list, wherever siblings are listed (in the same `endpoints/mod.rs`).
- Read-only query, so `Transactional::None` is used, the same as `get.rs`.
