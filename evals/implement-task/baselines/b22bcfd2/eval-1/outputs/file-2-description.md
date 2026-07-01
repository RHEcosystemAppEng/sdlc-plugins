# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Pre-Implementation Inspection

Before creating this file, inspect sibling endpoint handlers to match conventions:
- `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function in `modules/fundamental/src/advisory/endpoints/get.rs` to see exact parameter extraction, service invocation, and return pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` to see list handler structure
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` to see cross-module SBOM endpoint pattern (since the new endpoint is under the SBOM path)

## Detailed Changes

Create a new file with the following content:

```rust
//! Handler for the advisory severity summary endpoint.

use axum::{
    extract::Path,
    Json,
};
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use trustify_common::db::Transactional;

/// Returns aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts occurrences per severity
/// level (Critical, High, Medium, Low).
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: AdvisoryService,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Notes

- Parameter extraction pattern (`Path<Id>`) matches sibling `get.rs` handler
- Service invocation follows the same pattern as `fetch` and `list` calls in existing handlers
- Error wrapping with `.context()` matches the convention from `common/src/error.rs`
- The exact import paths and type names will be confirmed during code inspection (the `Id` type, `Transactional` import path, and `AdvisoryService` injection method need verification against siblings)
- Doc comment on the handler function explains what it does and how
- If the SBOM does not exist, the service method should return an appropriate error that maps to 404 via `AppError`
