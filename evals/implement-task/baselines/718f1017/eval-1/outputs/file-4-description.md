# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose
Define the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

## Detailed Changes

Create a new file:

```rust
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity breakdown (critical, high, medium, low, total) of
/// unique advisories linked to the given SBOM.
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
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Rationale
- Follows the pattern from `advisory/endpoints/get.rs`: extract `Path<Id>`, call service, return `Json<T>`
- Uses `State` extractor for the service (Axum pattern)
- `utoipa::path` attribute generates OpenAPI documentation matching the API contract
- Error handling via `AppError` with `.context()` wrapping
- 404 propagated from the service layer's SBOM existence check
