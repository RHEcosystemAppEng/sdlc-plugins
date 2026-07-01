# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Detailed Changes

Create a new file with the following content:

```rust
//! GET handler for advisory severity summary by SBOM.
//!
//! Returns aggregated severity counts (critical, high, medium, low, total)
//! for all advisories linked to a given SBOM.

use actix_web::web;
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Extracts the SBOM ID from the path, calls the advisory service to compute
/// severity counts, and returns the result as JSON. Returns 404 if the SBOM
/// does not exist.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    state: State<AdvisoryService>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = Transactional::new();
    let summary = state
        .severity_summary(id, &tx)
        .await
        .map_err(|e| e.into())?;
    Ok(Json(summary))
}
```

## Conventions Applied

- **File naming**: named after the resource concept (`severity_summary.rs`), matching sibling files `get.rs` and `list.rs`
- **Handler signature**: follows the pattern from `get.rs` -- extract path params via `Path<Id>`, call service method, return JSON
- **Error handling**: returns `Result<Json<T>, AppError>` matching all sibling handlers
- **Return type**: returns struct directly via Axum's `Json` extractor, as specified in Implementation Notes
- **Documentation**: `///` doc comment on the handler function and `//!` module-level documentation
- **Import organization**: standard library, external crates, then internal crate imports

## Notes

- The exact import paths and State extraction pattern would need to be confirmed by inspecting the actual `get.rs` sibling handler via Serena
- The `Id` type import and `Transactional` construction may vary based on the actual codebase patterns -- would be verified during Step 4
