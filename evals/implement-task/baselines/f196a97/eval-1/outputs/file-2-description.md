# File 2 -- CREATE: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Conventions Applied

- **Endpoint pattern:** Follows the pattern in sibling `get.rs` -- extract path params via `Path<Id>`, call service method, return JSON.
- **Error handling:** Returns `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping, matching `common/src/error.rs` pattern.
- **Handler function naming:** Named `severity_summary` following the `verb_noun` or descriptive pattern seen in siblings.
- **Documentation:** Handler function and all public items have `///` doc comments.

## Detailed Changes

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use common::db::Transactional;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// with counts per severity level (Critical, High, Medium, Low) and a total.
pub async fn severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Key Design Decisions

- Handler signature matches the existing `get.rs` pattern: `State` extractor for the service, `Path` for the SBOM ID, `Transactional` for database context.
- Error wrapping uses `.context()` to add a descriptive message, consistent with all handlers in the codebase.
- Returns `Json<SeveritySummary>` directly -- Axum handles serialization to JSON automatically.
- The 404 case is handled inside the service method (returning `AppError::NotFound` when the SBOM doesn't exist), not in the handler -- consistent with how `fetch` works in sibling services.
