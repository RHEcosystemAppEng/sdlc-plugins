# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls the `AdvisoryService::severity_summary` method and returns the result as JSON.

## Pre-implementation inspection

Before creating, inspect sibling endpoint files to understand the exact handler pattern:
1. `modules/fundamental/src/advisory/endpoints/get.rs` -- GET /api/v2/advisory/{id}: path parameter extraction, service call, JSON response, error handling.
2. `modules/fundamental/src/advisory/endpoints/list.rs` -- GET /api/v2/advisory: list handler pattern for comparison.
3. `modules/fundamental/src/sbom/endpoints/get.rs` -- GET /api/v2/sbom/{id}: SBOM-scoped handler for cross-module pattern confirmation.

## File contents

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
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. Deduplicates advisories by ID before counting.
/// Returns 404 if the SBOM ID does not exist.
pub async fn severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .map_err(AppError::from)?;

    Ok(Json(summary))
}
```

## Design decisions

- **Handler signature:** Matches the pattern in `advisory/endpoints/get.rs` -- `Path<Id>` for path parameter, `State<AdvisoryService>` for service injection, `Transactional<'_>` for database context.
- **Return type:** `Result<Json<SeveritySummary>, AppError>` -- Axum's `Json` extractor handles serialization; `AppError` implements `IntoResponse` for error mapping (including 404).
- **Error mapping:** `.map_err(AppError::from)` converts the `anyhow::Error` from the service layer into an `AppError` that Axum can render as an HTTP response. The service layer is responsible for returning the appropriate error type (e.g., not-found errors map to 404).
- **No pagination:** This endpoint returns a single aggregated summary, not a list -- so `PaginatedResults<T>` is not used.

## Conventions applied

- **Error handling:** `Result<T, AppError>` return type with error conversion, matching `common/src/error.rs` pattern
- **Path extraction:** `Path(id): Path<Id>` -- matching sibling endpoint handlers
- **State injection:** `State(service): State<AdvisoryService>` -- matching sibling endpoint handlers
- **Documentation:** `///` doc comment on the handler function
- **Import organization:** External crate imports first (`axum`), then internal crate imports (`crate::`, `common::`)
