# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This endpoint aggregates severity counts for advisories linked to a given SBOM and returns a `SeveritySummary` response.

## Sibling Reference

Follows the pattern of `modules/fundamental/src/advisory/endpoints/get.rs` for:
- Path parameter extraction via `Path<Id>`
- Service invocation pattern
- Error handling with `AppError` and `.context()`
- Response type (return struct directly, Axum's `Json` handles serialization)

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

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all unique advisories linked to the
/// specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

## Key Design Decisions

- **Parameter pattern**: Matches the existing `get.rs` pattern exactly -- `State(service)`, `Path(id)`, `tx: Transactional<'_>`
- **Error handling**: Uses `.context()` wrapping returning `AppError`, consistent with `common/src/error.rs` patterns and all other handlers in the project
- **Return type**: Returns `Json<SeveritySummary>` directly (not `PaginatedResults` since this is an aggregation, not a list)
- **404 handling**: The service method (`severity_summary`) checks for SBOM existence and returns an appropriate error if not found; the `.context()` wrapper propagates it as `AppError`
- **Doc comment**: Handler function has a documentation comment explaining what it does

## Integration

This handler is registered in the router by the change to `modules/fundamental/src/advisory/endpoints/mod.rs` (see file-5-description.md).
