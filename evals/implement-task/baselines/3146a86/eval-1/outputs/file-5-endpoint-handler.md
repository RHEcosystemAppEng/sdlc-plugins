# File 5 — Create: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose

Implement the HTTP GET handler for `/api/v2/sbom/{id}/advisory-summary`. This handler
extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary`, and
returns a JSON-serialized `SeveritySummary`. It mirrors the structure of the sibling
`get.rs` handler.

## Reference Pattern (from sibling `get.rs`)

```rust
// modules/fundamental/src/advisory/endpoints/get.rs (inferred from sibling inspection)
pub async fn get_advisory(
    Path(id): Path<Id>,
    State(service): State<Arc<AdvisoryService>>,
) -> Result<Json<AdvisoryDetails>, AppError> {
    let advisory = service
        .fetch(id, &Transactional::None)
        .await
        .context("failed to fetch advisory")?
        .ok_or_else(|| AppError::NotFound(format!("advisory {id} not found")))?;

    Ok(Json(advisory))
}
```

## Full File Content

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::advisory::AdvisoryService;
use common::error::AppError;
use axum::extract::{Path, State};
use axum::Json;
use sea_orm::TransactionTrait;
use std::sync::Arc;
use trustify_common::db::Transactional;
use trustify_common::id::Id;
use anyhow::Context;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns per-severity advisory counts for the specified SBOM. Returns 404
/// if no SBOM with the given ID exists. All severity levels default to 0
/// when the SBOM has no linked advisories.
pub async fn get_advisory_summary(
    Path(id): Path<Id>,
    State(service): State<Arc<AdvisoryService>>,
) -> Result<Json<SeveritySummary>, AppError> {
    // Verify the SBOM exists before computing the summary. Use the sbom service
    // or rely on the severity_summary method returning a 404-triggering error.
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

## 404 Behavior

The task requires a 404 when the SBOM ID does not exist. Two options:

**Option A (preferred — consistent with sibling pattern):** The `AdvisoryService::severity_summary` method returns an `Err` with a "not found" context when the SBOM ID doesn't exist in the `sbom` table. `AppError` converts this to HTTP 404 via `IntoResponse`.

**Option B:** Call the SBOM service to explicitly check SBOM existence before calling `severity_summary`. This adds a dependency on `SbomService` in the advisory endpoint, which breaks module isolation.

Option A is preferred. The service method will perform an existence check internally by querying the `sbom` entity before querying `sbom_advisory`, returning `AppError::NotFound` when appropriate.

## Handler Documentation

The `///` doc comment above the handler function satisfies the "documentation on new symbols" code quality practice from Step 6.

## Inspection Steps

1. `mcp__serena_backend__find_symbol` with `include_body=true` on `get_advisory` in `modules/fundamental/src/advisory/endpoints/get.rs` — confirm exact import paths for `Path`, `State`, `Json`, `AppError`, `Transactional`, `Id`.
2. `mcp__serena_backend__get_symbols_overview` on `common/src/error.rs` — confirm `AppError` variant names (especially the not-found variant).
3. Write the file using the Write tool (new file).
