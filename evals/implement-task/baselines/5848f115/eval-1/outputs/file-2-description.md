# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

New endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Pre-implementation analysis

Before creating this file, inspect sibling endpoint files to discover conventions:
- Read `modules/fundamental/src/advisory/endpoints/get.rs` via `mcp__serena_backend__find_symbol` with `include_body=true` to understand the exact handler function signature, `Path<Id>` extraction, service call pattern, and error handling.
- Read `modules/fundamental/src/advisory/endpoints/list.rs` via `mcp__serena_backend__get_symbols_overview` to confirm route handler patterns.
- Read `modules/fundamental/src/sbom/endpoints/get.rs` via `mcp__serena_backend__get_symbols_overview` for cross-module endpoint convention confirmation.
- Check `common/src/error.rs` via `mcp__serena_backend__find_symbol("AppError", include_body=true)` to understand `AppError` variants and `.context()` usage.

## Detailed changes

Create the file with the following content structure:

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use anyhow::Context;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated vulnerability advisory severity counts for the specified SBOM.
pub async fn handler(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions applied

- Handler function signature matches `advisory/endpoints/get.rs` pattern: `State`, `Path<Id>`, `Transactional` extractors
- Returns `Result<Json<T>, AppError>` matching all sibling handlers
- Uses `.context()` for error wrapping (matching `common/src/error.rs` pattern)
- Single-entity response (not paginated) since this returns an aggregation, not a list
- `///` doc comment on the handler function
- Import organization follows sibling patterns: framework imports, then internal crate imports
