# File 5: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

## Pattern Reference
Follows the endpoint pattern in `modules/fundamental/src/advisory/endpoints/get.rs`: extract path params via `Path<Id>`, call service method, return JSON response.

## Content

```rust
use actix_web::web;
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use trustify_common::error::AppError;
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories grouped by severity
/// level for the specified SBOM.
pub async fn get_severity_summary(
    service: State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to compute severity summary")?;

    Ok(Json(summary))
}
```

## Notes
- Follows exact same pattern as `get.rs` handler: `Path<Id>` extraction, service call, `Json` return
- Error handling uses `Result<Json<T>, AppError>` with `.context()` wrapping
- Single responsibility: extracts parameters, delegates to service, returns response
- Documentation comment explaining what the handler does
