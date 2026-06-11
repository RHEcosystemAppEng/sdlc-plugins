# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action:** CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service method, and returns the severity summary as JSON.

## Detailed Changes

### Handler function

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity count summary for all unique advisories
/// linked to the specified SBOM.
pub async fn get_severity_summary(
    service: axum::Extension<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(&id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design rationale

- **Path parameter extraction:** Uses `Path<Id>` to extract the SBOM ID, matching the pattern in `get.rs` (sibling endpoint handler).
- **Service invocation:** Calls `AdvisoryService::severity_summary` with the SBOM ID and transaction context, following the same pattern as `fetch` and `list` calls in sibling handlers.
- **Error handling:** Uses `Result<T, AppError>` with `.context()` wrapping, consistent with all endpoint handlers in the codebase per `common/src/error.rs`.
- **Response type:** Returns `Json<SeveritySummary>` directly — Axum handles serialization. This is a single-entity response (not paginated), matching the pattern for detail/summary endpoints.
- **404 handling:** The service method will return an `AppError` (not found) when the SBOM ID does not exist, which propagates through the `?` operator and results in a 404 response, consistent with existing SBOM endpoints.

### Conventions followed

- Handler function signature matches siblings in `endpoints/get.rs` and `endpoints/list.rs`.
- Import structure follows existing handler files.
- Error context string is descriptive and action-oriented.
- Doc comment on the handler function describes what the endpoint does.
