# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: Create (new file)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns advisory severity counts for a given SBOM. This follows the endpoint pattern established in `advisory/endpoints/get.rs`.

## Content

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use trustify_common::error::AppError;
use trustify_common::id::Id;

/// Returns advisory severity counts for the specified SBOM.
///
/// Aggregates advisories linked to the SBOM, deduplicates by advisory ID,
/// and returns counts per severity level (Critical, High, Medium, Low) and
/// total.
pub async fn get_severity_summary(
    service: /* injected AdvisoryService */,
    Path(id): Path<Id>,
    tx: /* injected Transactional */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Pattern source**: Follows the exact pattern in `advisory/endpoints/get.rs` -- extract path params via `Path<Id>`, call service method, return `Json` response.
- **Error handling**: Uses `Result<Json<SeveritySummary>, AppError>` return type with `.context()` wrapping, matching the convention in `common/src/error.rs`.
- **404 handling**: The service method handles SBOM-not-found by returning an appropriate `AppError` that maps to a 404 HTTP response, consistent with existing SBOM endpoints.
- **Response type**: Returns `SeveritySummary` directly wrapped in `Json` -- Axum handles serialization automatically.
- **Documentation**: The handler function has a `///` doc comment explaining what it does.

## Notes

The exact import paths and parameter extraction patterns (e.g., whether `Transactional` is injected via Axum state or web::Data) must be confirmed by inspecting the existing `get.rs` endpoint during implementation. The above is a representative structure based on the task's Implementation Notes.
