# File 2: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` as JSON.

## Pre-Implementation Inspection

Before creating this file, inspect:
- **`modules/fundamental/src/advisory/endpoints/get.rs`** — Examine the existing GET handler pattern: how `Path<Id>` is extracted, how the service is invoked, how `Result<T, AppError>` is returned, and how `Json` wraps the response.
- **`modules/fundamental/src/sbom/endpoints/get.rs`** — Cross-module sibling endpoint handler for additional pattern confirmation.
- **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Understand how handlers are imported and routes are registered.

## Changes

Create a new file with the following content:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::advisory::AdvisoryService;
use axum::extract::{Path, State};
use axum::Json;
use common::error::AppError;
use trustify_common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. Deduplicates advisories by ID before counting.
pub async fn handler(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Path extraction**: Uses `Path<Id>` extractor following the pattern in `advisory/endpoints/get.rs`.
- **State extraction**: Uses `State<AdvisoryService>` to access the service, matching existing handlers.
- **Error handling**: Returns `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping, matching the `common/src/error.rs` pattern.
- **Response type**: Returns the struct directly via `Json<SeveritySummary>`; Axum handles serialization.
- **Documentation**: Handler function has a doc comment explaining what it does, following the code quality practice requirement.
- **File naming**: Named `severity_summary.rs` after the feature, consistent with `get.rs` and `list.rs` naming in the endpoints directory.
