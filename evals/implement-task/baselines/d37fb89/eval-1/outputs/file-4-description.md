# File 4: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Action: CREATE

## Purpose
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` following the established endpoint pattern from `advisory/endpoints/get.rs`.

## Conventions Applied
- Async handler function returning `Result<Json<T>, AppError>` (sibling pattern from `get.rs`, `list.rs`)
- Path parameter extraction via `Path<Id>` (Axum extractor pattern)
- Service invoked via Axum shared state
- Error handling returns `AppError` with `.context()` wrapping
- Documentation comment on the handler function

## Detailed Changes

Create a new file with the following content:

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. Counts are broken down by severity level (critical,
/// high, medium, low) with a total.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
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
- The handler follows the exact pattern from `advisory/endpoints/get.rs`: extract path params, call service, return JSON
- `State<AdvisoryService>` is the Axum state injection pattern used by sibling handlers
- `Transactional` is passed through to the service method, maintaining the transaction-aware pattern
- The handler is thin -- all business logic (SBOM existence check, deduplication, counting) lives in the service layer, following separation of concerns
- Documentation comment explains the endpoint's behavior and response structure
