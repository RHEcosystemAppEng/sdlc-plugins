# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns a `SeveritySummary` JSON response containing aggregated severity counts for all advisories linked to the specified SBOM.

## Sibling Reference

- `modules/fundamental/src/advisory/endpoints/get.rs` — primary pattern reference for single-resource GET handler (path extraction, service call, JSON response, error handling)
- `modules/fundamental/src/sbom/endpoints/get.rs` — cross-module reference for SBOM-scoped endpoint patterns

## Content

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use std::sync::Arc;

use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::advisory::AdvisoryService,
};
use trustify_common::db::Transactional;
use trustify_common::error::AppError;
use trustify_common::id::Id;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn get_severity_summary(
    State(service): State<Arc<AdvisoryService>>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, Transactional::None)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

## Conventions Followed

- Handler is a standalone `async fn`, not a method on a struct — matches `get.rs` pattern
- Path parameter extracted via `Path<Id>` — matches existing advisory and SBOM GET handlers
- Service obtained via `State<Arc<AdvisoryService>>` — matches Axum state injection pattern
- Returns `Result<Json<SeveritySummary>, AppError>` — matches existing handler return types
- Error propagation uses `.context()` wrapping — matches `common/src/error.rs` convention
- `#[utoipa::path]` attribute for OpenAPI documentation — matches existing endpoint annotations
- 404 handling delegated to the service layer (service returns `AppError::NotFound` when SBOM does not exist)

## Notes

- The exact import paths for `Transactional`, `Id`, and `AppError` should be confirmed by inspecting the actual sibling `get.rs` file during the pre-implementation analysis phase
- The `#[utoipa::path]` attribute may need adjustment based on the exact utoipa version and configuration used in the project
