# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Pre-implementation inspection
- Read `modules/fundamental/src/advisory/endpoints/get.rs` (sibling) to understand the exact handler pattern: function signature, extractors, service invocation, return type, error handling, imports.
- Read `modules/fundamental/src/advisory/endpoints/list.rs` (sibling) for additional pattern confirmation.
- Read `modules/fundamental/src/sbom/endpoints/get.rs` (cross-module sibling) to confirm patterns are consistent across modules.

## Detailed Changes

### New handler function

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use common::db::Transactional;

/// Handle GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. Responds with a `SeveritySummary` containing counts
/// for critical, high, medium, low, and total severity levels.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,  // or State, depending on sibling pattern
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

### Conventions followed
- Function signature matches `get.rs` sibling: `Path<Id>` extractor, service injection (Extension or State -- determined from sibling analysis), transaction parameter.
- Returns `Result<Json<T>, AppError>` matching sibling handlers.
- Error wrapping uses `.context()` matching `common/src/error.rs` patterns.
- Doc comment on the handler function.
- File is named after the feature (`severity_summary.rs`), following the naming pattern of `get.rs`, `list.rs`.
- Imports follow the same organization as sibling handler files.

### Notes
- The exact extractor type for the service (Extension vs State) would be determined by reading the sibling `get.rs` handler.
- The exact type for `Id` would be determined from sibling analysis (could be `Uuid`, `i32`, or a custom type).
- The transaction extractor pattern would be confirmed from sibling handlers.
