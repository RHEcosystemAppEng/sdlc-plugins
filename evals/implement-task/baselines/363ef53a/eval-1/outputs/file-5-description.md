# File 5: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

**Action:** Create new file

## Pre-implementation inspection

Before writing this file, read the sibling endpoint handler `modules/fundamental/src/advisory/endpoints/get.rs` using `mcp__serena_backend__find_symbol` with `include_body=true` to understand the full handler implementation pattern: path parameter extraction, service invocation, JSON response return, and error handling.

Also inspect `common/src/error.rs` to confirm `AppError` usage and the `.context()` error wrapping pattern.

## Contents

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary`:

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories by severity level
/// (Critical, High, Medium, Low) and a total count for the specified SBOM.
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService -- follow existing injection pattern from get.rs */,
    tx: /* Transactional -- follow existing pattern */,
) -> Result<Json<SeveritySummary>, AppError> {
    // Call the service method
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

**Pattern conformance:**
- Follows the exact handler pattern from `advisory/endpoints/get.rs`:
  - `Path<Id>` for path parameter extraction
  - Service and transaction injected via Axum extractors (match the exact injection mechanism used in `get.rs`)
  - Returns `Result<Json<T>, AppError>`
  - Uses `.context()` for error wrapping
- Includes a `///` documentation comment describing the handler's behavior
- Returns 404 via AppError when the SBOM ID does not exist (the service method returns an appropriate error that AppError maps to 404)

**Error handling:**
- The service method should return an error when the SBOM ID is not found
- `.context()` wrapping provides descriptive error messages
- `AppError`'s `IntoResponse` implementation maps the error to the appropriate HTTP status code (404 for not-found)
