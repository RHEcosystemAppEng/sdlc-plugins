# File 5: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service method, and returns the severity summary as JSON.

## Content

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns an aggregated severity summary (critical, high, medium, low, total)
/// for all unique advisories linked to the specified SBOM. Returns 404 if the
/// SBOM ID does not exist.
pub async fn get_severity_summary(
    service: /* extracted AdvisoryService (via Axum state or extension) */,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    // Call the service method to compute severity counts
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

## Pattern Compliance

- **Handler signature**: follows the pattern in `modules/fundamental/src/advisory/endpoints/get.rs`:
  - Extract path params via `Path<Id>`
  - Receive service via Axum's dependency injection (state/extension)
  - Accept `Transactional` for database transaction context
  - Return `Result<Json<T>, AppError>`
- **Error handling**: uses `.context()` wrapping matching `common/src/error.rs` pattern
- **Response type**: returns struct directly wrapped in `Json()` -- Axum handles serialization
- **Documentation**: handler function has a doc comment describing the endpoint, HTTP method, response, and error behavior
- **Naming**: `get_severity_summary` follows `<verb>_<resource>` convention seen in sibling handlers

## Data Flow

1. Axum extracts `id` from path segment `{id}` via `Path<Id>`
2. Handler calls `service.severity_summary(id, &tx)`
3. Service queries database, deduplicates, counts severities
4. Service returns `SeveritySummary` or `AppError`
5. Handler wraps successful result in `Json()` and returns
6. On error, `AppError` implements `IntoResponse` for proper HTTP error codes (e.g., 404)

## Impact

- New file, no existing code affected
- Handler is registered by the route in `endpoints/mod.rs` (file 3)
