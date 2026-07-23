# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Implement the GET handler for `GET /api/v2/sbom/{id}/advisory-summary`. This handler extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary()`, and returns the result as JSON.

## Pre-implementation inspection

Before creating this file, inspect these sibling files to understand the endpoint handler pattern:

- **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Read via `mcp__serena_backend__find_symbol` with `include_body=true` to see the full GET handler implementation: how `Path<Id>` is used for path parameter extraction, how the service is obtained from Axum state, how the service method is called, and how `Result<Json<T>, AppError>` is returned. This is the primary template.
- **`modules/fundamental/src/sbom/endpoints/get.rs`** -- Read to confirm cross-module consistency in GET handler patterns.
- **`common/src/error.rs`** -- Read via `mcp__serena_backend__find_symbol` for the `AppError` type to confirm the error handling and `.context()` usage pattern.

## Detailed changes

Create the file with the following content:

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// enabling dashboard widgets to render severity breakdowns.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve severity summary")?;

    Ok(Json(summary))
}
```

## Conventions followed

- Uses `Path<Id>` for path parameter extraction (matches `advisory/endpoints/get.rs` pattern)
- Calls service method and returns `Result<Json<T>, AppError>` (matches sibling handlers)
- Uses `.context()` for error wrapping (matches `common/src/error.rs` pattern)
- Includes documentation comment on the handler function
- Import organization follows the established order: axum, local crate, common crate
