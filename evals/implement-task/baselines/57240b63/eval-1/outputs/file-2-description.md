# File 2: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose
Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Reference Files to Inspect First
- `modules/fundamental/src/advisory/endpoints/get.rs` -- Primary reference for the endpoint handler pattern: Path<Id> extraction, service invocation, JSON response return, and error handling.
- `common/src/error.rs` -- Understand AppError and how it converts to HTTP responses (e.g., 404 for not found).

## Changes

Create a new file with the following content (structure follows the pattern in `get.rs`):

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use actix_web::{web, HttpResponse};  // Or axum equivalents -- confirm from get.rs
use trustify_common::error::AppError;
use trustify_common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM.
pub async fn get_advisory_severity_summary(
    path: web::Path<Id>,  // Exact extraction type from get.rs pattern
    service: web::Data<AdvisoryService>,  // Or however the service is injected
    tx: web::Data<Transactional<'_>>,
) -> Result<HttpResponse, AppError> {
    let id = path.into_inner();
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to fetch advisory severity summary")?;
    Ok(HttpResponse::Ok().json(summary))
}
```

## Notes
- The exact import paths, extraction types (Axum `Path<Id>` vs Actix `web::Path<Id>`), and service injection mechanism must be confirmed by reading `get.rs` before implementation.
- Error handling follows the `Result<T, AppError>` with `.context()` wrapping pattern from `common/src/error.rs`.
- The handler returns 404 implicitly when the service method returns a not-found error via AppError.
- The response type (`SeveritySummary`) is returned directly via JSON serialization, as described in the Implementation Notes.
