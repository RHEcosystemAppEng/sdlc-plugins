# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

## Changes

Create new file with the following content:

```rust
use axum::{extract::Path, Json};
use axum::extract::State;
use std::sync::Arc;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// GET handler that returns severity counts for advisories linked to an SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found")
    )
)]
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<Arc<AdvisoryService>>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching severity summary")?;

    Ok(Json(summary))
}
```

## Rationale
- Follows the exact endpoint pattern from `advisory/endpoints/get.rs`: `Path<Id>` extraction, `State<Arc<Service>>`, `Transactional<'_>`, returns `Result<Json<T>, AppError>`
- Uses `.context()` error wrapping matching `common/src/error.rs` pattern
- Includes `utoipa::path` annotation for OpenAPI documentation consistency
