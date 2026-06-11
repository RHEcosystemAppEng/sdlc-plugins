# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: Create new file

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This endpoint extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the aggregated severity counts as JSON.

## Detailed Changes

```rust
use actix_web::web;
use axum::{
    extract::Path,
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use trustify_common::error::AppError;
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// Retrieve aggregated advisory severity counts for a given SBOM.
///
/// Returns the number of unique advisories at each severity level
/// (Critical, High, Medium, Low) and a total count.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "The SBOM identifier")
    ),
    responses(
        (status = 200, description = "Advisory severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found")
    )
)]
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

## Conventions Applied

- **Handler pattern**: follows the exact pattern from `advisory/endpoints/get.rs` -- extract `Path<Id>`, call service, return `Json<T>`
- **Error handling**: returns `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping, matching `common/src/error.rs` pattern
- **Response type**: returns struct directly via Axum's `Json` extractor (as specified in Implementation Notes)
- **OpenAPI annotation**: `#[utoipa::path]` attribute for API documentation generation, consistent with sibling endpoints
- **Documentation**: doc comment on the handler function explaining what it does
- **File naming**: named `severity_summary.rs` following the action-based naming pattern of sibling files (`get.rs`, `list.rs`)

## Notes

- The exact import paths and framework extractors would be confirmed by inspecting sibling endpoint files via Serena (`mcp__serena_backend__find_symbol`) before implementation
- If the project uses Actix-web extractors vs Axum extractors, the pattern would be adjusted accordingly based on what is found in `get.rs`
