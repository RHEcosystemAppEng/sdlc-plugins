# File 4: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary`, and returns the result as JSON.

## Detailed Changes

### Imports

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use common::db::Transactional;
```

### Handler Function

```rust
/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts for all advisories linked to the specified SBOM.
/// Responds with a JSON object containing critical, high, medium, low, and total counts.
/// Returns 404 if the SBOM ID does not exist.
pub async fn severity_summary(
    Path(id): Path<Id>,
    service: AdvisoryService,  // extracted via Axum's state/extension mechanism
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    // Given: SBOM ID from path parameter

    // When: call the service to compute severity summary
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to get advisory severity summary for SBOM")?;

    // Then: return the summary as JSON
    Ok(Json(summary))
}
```

### Design Decisions

- **Handler pattern**: Follows the exact pattern from `advisory/endpoints/get.rs` -- extract `Path<Id>`, call service method, return `Json(result)`.
- **Error propagation**: Uses `.context()` for error wrapping, which maps to appropriate HTTP status codes via `AppError`'s `IntoResponse` implementation.
- **Service extraction**: The `AdvisoryService` is injected via Axum's state extraction mechanism, matching how existing handlers receive the service.
- **Transaction parameter**: The `Transactional` extractor is used consistently with sibling handlers.
- **Documentation**: The handler function has a `///` doc comment describing what it does, its response format, and error behavior.

### Sibling Parity

Matches the structure of `advisory/endpoints/get.rs`:
- Same parameter extraction pattern (`Path<Id>`)
- Same service call pattern
- Same return type pattern (`Result<Json<T>, AppError>`)
- Same error wrapping with `.context()`
