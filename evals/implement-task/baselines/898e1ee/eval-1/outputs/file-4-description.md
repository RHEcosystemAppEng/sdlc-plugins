# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the result as JSON.

## Sibling files inspected

- `modules/fundamental/src/advisory/endpoints/get.rs` -- GET handler for `/api/v2/advisory/{id}`. Uses `Path<Id>` extractor, calls service method, returns `Result<Json<T>, AppError>`. This is the primary template.
- `modules/fundamental/src/advisory/endpoints/list.rs` -- GET handler for `/api/v2/advisory`. Uses query params for filtering/pagination, returns paginated results.
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET handler for `/api/v2/sbom/{id}`. Cross-module sibling for SBOM-scoped endpoint pattern.

## Conventions applied

- Handler function signature: `async fn handler(Path(id): Path<Id>, ...) -> Result<Json<T>, AppError>`
- Service is injected via Axum state/extension (matching how `get.rs` accesses AdvisoryService)
- Error handling returns `AppError` with `.context()` wrapping
- Response type is `Json<SeveritySummary>` (Axum serializes automatically)
- Documentation comment on the handler function

## Detailed changes

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
/// Returns aggregated severity counts (critical, high, medium, low, total)
/// for all advisories linked to the specified SBOM.
pub async fn get_advisory_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Rationale

- Follows the exact same pattern as `get.rs`: extract path param via `Path<Id>`, get service from state, call async service method, return `Json` result.
- The handler is thin -- all business logic lives in the service layer, consistent with the codebase's separation of concerns.
- Error handling delegates to AppError, which implements Axum's `IntoResponse` trait for proper HTTP error responses.
- The function is `pub` so it can be imported by `endpoints/mod.rs` for route registration.
