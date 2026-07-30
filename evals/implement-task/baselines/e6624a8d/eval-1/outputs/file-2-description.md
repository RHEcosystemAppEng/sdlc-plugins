# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, delegates to the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` as a JSON response.

## Detailed Changes

### Handler function

```rust
use anyhow::Context;
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::db::Transactional;
use trustify_common::error::AppError;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;

/// Returns aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the advisory service for all advisories associated with the SBOM
/// identified by `id`, groups them by severity level, and returns the counts.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = String, Path, description = "The SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Severity summary for the SBOM's advisories", body = SeveritySummary),
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
- **Transaction parameter**: Accepts `Transactional<'_>` as a parameter, following the convention used by `fetch` and `list` handlers for transaction-aware database access.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` matches the standard handler signature pattern for single-entity responses.
- **Error handling**: Uses `.context()` wrapping from anyhow to produce descriptive error messages, consistent with `common/src/error.rs`.
- **OpenAPI annotations**: Uses `#[utoipa::path(...)]` macro with `params` and `responses` specifications for API documentation generation, consistent with existing endpoint handlers.
- **File placement**: Separate handler file under `endpoints/`, following the same pattern as `get.rs` and `list.rs`.
- **Doc comment**: Documents the handler function purpose as required by the skill's code quality practices.
