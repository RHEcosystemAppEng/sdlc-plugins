# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls the service layer and returns the `SeveritySummary` as JSON.

## Detailed Changes

### Handler function

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::error::AppError;
use trustify_common::db::Transactional;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the given SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = String, Path, description = "The SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<String>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(&id, &tx)
        .await
        .context("Failed to fetch severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Followed

- **Parameter extraction**: Uses `Path<String>` for the SBOM ID, consistent with `get.rs` in both the advisory and sbom endpoint modules.
- **State extraction**: Extracts the service from Axum shared state via `State<AdvisoryService>`, matching the pattern in existing handlers.
- **Transaction parameter**: Accepts `Transactional<'_>` as a parameter, following the convention used by `fetch` and `list` handlers.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` matches the standard handler signature pattern.
- **Error handling**: Uses `.context()` wrapping to produce descriptive error messages, matching the pattern in `common/src/error.rs`.
- **OpenAPI annotations**: Uses `#[utoipa::path(...)]` macro for API documentation generation, consistent with existing endpoint handlers.
- **File placement**: Separate handler file under `endpoints/`, following the same pattern as `get.rs` and `list.rs`.
