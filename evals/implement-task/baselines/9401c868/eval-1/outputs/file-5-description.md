# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns advisory severity counts for a given SBOM.

## Pre-Implementation Analysis

Before creating, would analyze sibling endpoint files:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand handler pattern (Path extraction, service call, JSON response)
- `mcp__serena_backend__find_symbol` with `include_body=true` on the `get` handler in `advisory/endpoints/get.rs` -- read the full handler implementation
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module endpoint comparison

## File Content

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
use common::id::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// with counts for Critical, High, Medium, and Low severity levels plus
/// a total count of unique advisories.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Default::default())
        .await
        .context("failed to get advisory severity summary")?;

    Ok(Json(summary))
}
```

## Key Decisions

- **Handler pattern**: Follows the exact pattern from `advisory/endpoints/get.rs` -- extract path params via `Path<Id>`, extract service via `State<AdvisoryService>`, call service method, return `Json<T>`
- **Error handling**: Returns `Result<T, AppError>` with `.context()` wrapping, matching established convention
- **Return type**: Returns `Json<SeveritySummary>` directly -- Axum handles serialization to JSON response
- **Transaction**: Uses `Default::default()` for the transactional parameter, matching existing non-write endpoint patterns
- **Documentation**: Doc comment on the handler function explaining the endpoint, parameters, and response
- **Defensive access**: Error context wraps the service call to provide meaningful error messages
- **404 handling**: The service method handles 404 when SBOM does not exist, consistent with existing SBOM endpoints (AppError propagation)
