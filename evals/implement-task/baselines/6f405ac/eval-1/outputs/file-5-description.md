# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Full File Contents

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns an aggregated severity summary (critical, high, medium, low, total)
/// for all vulnerability advisories linked to the specified SBOM. Returns 404
/// if the SBOM ID does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = Transactional::none();

    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Followed

- **Path extraction**: Uses `Path<Id>` extractor matching the pattern in `endpoints/get.rs`
- **State extraction**: Uses `State<AdvisoryService>` for service injection via Axum state
- **Return type**: `Result<Json<SeveritySummary>, AppError>` matching all sibling handlers
- **Error handling**: Uses `.context()` wrapping for error messages, returning `AppError`
- **Transaction**: Creates a `Transactional::none()` for read-only queries (matching `fetch` pattern)
- **JSON response**: Returns the struct directly wrapped in `Json()` as noted in implementation notes
- **Documentation**: Handler function has `///` doc comment explaining the endpoint's behavior
- **Import organization**: Standard library, external crates (axum), then internal modules
- **404 behavior**: The service method would return an error when the SBOM ID does not exist; `AppError` maps this to a 404 response consistent with existing SBOM endpoints
