# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Pre-Implementation Inspection

Read the sibling endpoint handler `modules/fundamental/src/advisory/endpoints/get.rs` using `mcp__serena_backend__find_symbol` to understand the exact pattern for path parameter extraction, service calls, and JSON response handling. This file is the primary template for the new endpoint.

## New File Content

```rust
//! GET handler for advisory severity summary endpoint.

use actix_web::web;
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of critical, high, medium, and low
/// advisories linked to the specified SBOM.
pub async fn get(
    service: web::Data<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

This follows the exact pattern from `advisory/endpoints/get.rs`:
- Path parameter extracted via `Path<Id>`
- Service called with the ID and transaction
- Response returned as `Json<SeveritySummary>`
- Error handling uses `Result<T, AppError>` with `.context()` wrapping
- Returns 404 when SBOM ID does not exist (handled by the service layer's AppError)
