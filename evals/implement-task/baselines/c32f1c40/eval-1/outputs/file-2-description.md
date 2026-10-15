# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the
SBOM ID from the path, calls the advisory service, and returns the severity summary
as JSON.

## Detailed Changes

### Handler Implementation

```rust
use actix_web::web;
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// Retrieves aggregated advisory severity counts for a given SBOM.
///
/// Returns a JSON object with counts per severity level (critical, high, medium, low)
/// and a total count of unique advisories. Returns 404 if the SBOM does not exist.
pub async fn severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design Decisions

- **Follows `get.rs` pattern**: uses the same extractor pattern (`Path<Id>`, `State`,
  `Transactional`) as the existing `get.rs` handler for consistency.
- **Error handling**: wraps the service call with `.context()` matching the `AppError`
  pattern in `common/src/error.rs`. The service will return a 404 error if the SBOM
  does not exist, which propagates through `AppError`.
- **Returns `Json<SeveritySummary>`**: Axum automatically serializes the struct to JSON.
- **Doc comment**: documents the endpoint behavior including the 404 case.

### Convention Conformance

- Handler signature matches sibling `get.rs`: `async fn` taking State, Path, Transactional,
  returning `Result<Json<T>, AppError>`.
- Error wrapping with `.context()` follows the project convention.
- File name `severity_summary.rs` follows the `verb_noun`/descriptive pattern of
  sibling files `get.rs`, `list.rs`.
