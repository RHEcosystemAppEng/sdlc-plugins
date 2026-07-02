# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` as a JSON response.

## Detailed Changes

### Handler Function

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
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design Decisions

- **Path extraction**: Uses `Path<Id>` matching the pattern in `endpoints/get.rs`.
- **State extraction**: Uses `State<AdvisoryService>` to access the service, following the existing handler pattern.
- **Transactional context**: Passes `&Transactional::None` following the convention in existing handlers for read-only queries.
- **Error handling**: Uses `.context()` wrapping with `AppError`, matching the error handling convention from `common/src/error.rs`.
- **Return type**: Returns `Result<Json<SeveritySummary>, AppError>` following the convention where the struct is returned directly and Axum handles serialization.

### Conventions Followed

- Function naming follows `get_<resource>` pattern (matches `get` in `get.rs`).
- Import organization: external crates first (axum), then internal modules (crate, common).
- Documentation comment on the handler function.
- Error message in `.context()` is descriptive and follows "Failed to ..." pattern.
