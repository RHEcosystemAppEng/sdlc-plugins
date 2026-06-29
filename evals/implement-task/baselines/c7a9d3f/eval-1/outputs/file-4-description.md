# File 4: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Action: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls the service method and returns the severity summary as JSON.

## Detailed Changes

Create a new endpoint handler file following the pattern in `get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories at each severity level
/// (Critical, High, Medium, Low) for the specified SBOM, plus a total count.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: AdvisoryService,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Key Implementation Details

1. **Path extraction**: uses `Path<Id>` to extract the SBOM ID from the URL path, matching the pattern in `get.rs`.

2. **Service injection**: receives `AdvisoryService` as an Axum extractor (following the DI pattern used by existing handlers).

3. **Transaction handling**: receives `Transactional<'_>` as an extractor and passes it to the service method.

4. **Error wrapping**: uses `.context()` to wrap errors with a descriptive message, following the `AppError` pattern from `common/src/error.rs`.

5. **JSON response**: returns `Json<SeveritySummary>` which Axum automatically serializes to JSON. This is the single-resource response pattern (not `PaginatedResults<T>` since this is an aggregation, not a list).

## Conventions Applied

- **Handler signature**: follows the same pattern as `get.rs` handlers with `Path<Id>` extraction.
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping.
- **Response type**: returns struct directly via `Json` extractor (not paginated).
- **Documentation**: doc comment on the handler function explaining the endpoint.
