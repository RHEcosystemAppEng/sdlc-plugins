# File 4: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose
Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls the `AdvisoryService::severity_summary` method and returns the result as JSON.

## Full File Content

```rust
//! Advisory severity summary endpoint.
//!
//! Provides a GET handler that returns aggregated advisory severity counts
//! for a given SBOM.

use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Returns aggregated severity counts for advisories linked to the specified SBOM.
///
/// Responds with a JSON object containing counts for each severity level
/// (critical, high, medium, low) and a total count.
///
/// Returns 404 if the SBOM ID does not exist.
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

## Conventions Applied
- Follows the exact pattern from `modules/fundamental/src/advisory/endpoints/get.rs`:
  - Extracts path params via `Path<Id>`
  - Extracts service via `State<AdvisoryService>`
  - Calls service method and returns `Json<T>`
  - Error handling via `Result<T, AppError>` with `.context()` wrapping
- Module-level and function-level doc comments using `///` convention.
- Import organization: axum framework imports first, then crate-level imports, then common imports.

## Notes
- The exact `State` extractor and `Transactional` usage depends on how the existing handlers inject dependencies. This follows the most likely Axum pattern based on the sibling `get.rs` handler.
- The `Id` type is whatever the project uses for SBOM identifiers (likely `uuid::Uuid` or a newtype wrapper).
