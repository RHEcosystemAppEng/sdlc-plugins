# File 5: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Change Type
Create new file

## Description
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This endpoint extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary`, and returns the result as JSON.

## Full File Content

```rust
//! Handler for the advisory severity summary endpoint.

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use axum::extract::Path;
use axum::Json;
use common::error::AppError;
use common::db::Transactional;

/// Returns an aggregated severity summary of advisories linked to the specified SBOM.
///
/// Responds with a JSON object containing counts for each severity level (critical,
/// high, medium, low) and a total count of unique advisories. Returns 404 if the
/// SBOM ID does not exist.
pub async fn get_severity_summary(
    service: axum::Extension<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .map_err(AppError::from)
        .context("failed to retrieve severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Followed
- Handler signature matches `advisory/endpoints/get.rs` pattern: `Path<Id>` extraction, service via Extension, `Transactional` parameter
- Return type is `Result<Json<T>, AppError>` matching all sibling endpoint handlers
- Error handling uses `.context()` wrapping consistent with `common/src/error.rs` pattern
- Response type returned directly via `Json()` wrapper (Axum handles serialization)
- Documentation comment on the public handler function explaining behavior, response, and error cases
- Module-level doc comment for the file
- Import organization: local crate imports, then axum, then common
