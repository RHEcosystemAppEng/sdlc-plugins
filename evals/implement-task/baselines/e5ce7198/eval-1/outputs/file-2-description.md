# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the AdvisoryService to compute severity counts, and returns the result as JSON.

## Detailed Changes

### Handler Function

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Retrieves aggregated advisory severity counts for a specific SBOM.
///
/// Returns the number of unique advisories at each severity level (critical,
/// high, medium, low) along with a total count.
pub async fn handler(
    service: /* extracted AdvisoryService -- exact extraction pattern from get.rs */,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design Decisions

- **Handler signature**: follows the exact pattern from `advisory/endpoints/get.rs` -- `Path<Id>` for path parameter extraction, service injected via Axum state/extension (exact mechanism determined by inspecting `get.rs`)
- **Error handling**: uses `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping, matching the established error handling convention
- **Return type**: returns `Json<SeveritySummary>` directly -- Axum handles serialization automatically
- **404 handling**: the service layer returns `AppError` with appropriate status when SBOM ID is not found; the handler propagates this via `?`

### Convention Compliance

- Doc comment on the handler function
- Uses `.context()` for error wrapping (matching `common/src/error.rs` pattern)
- Parameter extraction via `Path<Id>` (matching sibling endpoint patterns)
- Imports follow the same organization as sibling endpoint files
