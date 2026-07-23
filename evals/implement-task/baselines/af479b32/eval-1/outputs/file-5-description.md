# File 5: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose
Define the GET handler for the `/api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated severity counts.

## Full File Content

```rust
//! Advisory severity summary endpoint.
//!
//! Provides a GET handler that returns aggregated advisory severity counts
//! for a given SBOM, enabling dashboard widgets to render severity breakdowns
//! without client-side counting.

use actix_web::web;
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// Queries all advisories linked to the given SBOM, deduplicates by advisory ID,
/// and returns counts per severity level (Critical, High, Medium, Low) plus total.
///
/// # Errors
///
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_severity_summary(
    service: web::Data<AdvisoryService>,
    Path(id): Path<Id>,
    tx: web::Data<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions
- **Handler signature** follows the pattern in `advisory/endpoints/get.rs`: extract `Path<Id>`, call service, return `Json<T>`
- **Error handling** uses `.context()` wrapping matching `common/src/error.rs` patterns
- **Dependency injection** uses Axum/actix-web's data extractors for the service and transaction -- the exact extractor type should match whatever pattern `get.rs` uses (the above uses `web::Data` but should be confirmed against the actual `get.rs` implementation)
- **Return type** is `Result<Json<SeveritySummary>, AppError>` -- Axum handles serialization automatically
- **Doc comments** explain what the handler does, including the error case

## Notes
- The exact import paths and extractor types (Axum vs actix-web) should be confirmed by reading the actual `get.rs` sibling file. The repo description says "Axum for HTTP" so Axum extractors should be used. The code above shows a hybrid -- in actual implementation, use whichever pattern `get.rs` uses consistently.
- If the project uses `State` instead of `web::Data` for dependency injection, match that pattern.
