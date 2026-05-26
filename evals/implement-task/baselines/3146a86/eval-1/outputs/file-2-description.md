# File 2: CREATE — `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose
GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns severity counts.

## Changes

Create a new file with:

```rust
use actix_web::web;
use axum::extract::Path;
use axum::Json;

use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use trustify_common::error::AppError;
use trustify_common::db::Transactional;

/// GET handler for /api/v2/sbom/{id}/advisory-summary.
pub async fn get_severity_summary(
    service: web::Data<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to fetch severity summary")?;
    Ok(Json(summary))
}
```

## Conventions Applied

- Follows the endpoint pattern from `advisory/endpoints/get.rs`: extract path params via `Path<Id>`, call service method, return `Json` wrapper
- Error handling uses `Result<T, AppError>` with `.context()` wrapping, matching `common/src/error.rs`
- Function naming follows `get_<resource>` verb_noun convention seen in sibling endpoints
