# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Pre-implementation Inspection

Before creating, would inspect sibling endpoint files to match conventions:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/get.rs")` -- see handler function signature, Path extraction, service call, JSON return pattern.
2. `mcp__serena_backend__find_symbol("get", include_body=true)` in the `get.rs` file -- read the full handler implementation.
3. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/sbom/endpoints/get.rs")` -- cross-module sibling for additional pattern reference.

## File Content

```rust
//! Handler for the SBOM advisory severity summary endpoint.

use actix_web::web;
use axum::{
    extract::Path,
    Json,
};
use anyhow::Context;

use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// Queries all advisories linked to the given SBOM via the sbom_advisory join table,
/// deduplicates by advisory ID, and returns counts per severity level.
///
/// Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    Path(sbom_id): Path<Id>,
    service: axum::Extension<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Rationale

- **Handler signature**: follows the pattern from `modules/fundamental/src/advisory/endpoints/get.rs`:
  - `Path<Id>` for extracting the SBOM ID from the URL path
  - `axum::Extension<AdvisoryService>` for dependency injection of the service (pattern would be confirmed via Serena inspection -- could also be `State` depending on the project's Axum version)
  - `Transactional<'_>` for database transaction context
  - Returns `Result<Json<SeveritySummary>, AppError>`
- **Error handling**: uses `.context()` wrapping consistent with established convention.
- **Documentation**: handler function has a doc comment explaining behavior and error cases per skill Step 6 code quality requirements.
- **Imports**: would be finalized after inspecting sibling files to match exact import paths. The imports shown above are representative; the actual `Extension` vs `State` pattern and `Id` type import path would be confirmed from sibling inspection.
- **Thin handler**: the handler delegates all business logic to the service layer, keeping the endpoint handler focused on HTTP concerns (extraction, serialization, error mapping).

## Note on imports

The exact import paths (e.g., whether `Id` comes from `common::model::Id` or another location, whether the service is injected via `Extension` or `State`) would be confirmed by reading the sibling endpoint `get.rs` with Serena before writing this file. The code above represents the structural pattern; exact paths would match what the sibling uses.
