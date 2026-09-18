# File 5: GET Handler for Advisory Summary Endpoint

**File**: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
**Action**: CREATE

## Purpose

Implements the HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary`. Extracts
the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method,
and returns the result as JSON.

## Full File Content

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
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM. Each
/// severity level (critical, high, medium, low) contains the count of unique
/// advisories at that level. Returns 404 if the SBOM does not exist.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Advisory severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

1. **Path parameter extraction**: uses `Path<Id>` following the sibling pattern in
   `advisory/endpoints/get.rs`.

2. **State extraction**: uses `State<AdvisoryService>` to access the service from
   Axum's shared application state, following the existing handler pattern.

3. **Transaction context**: accepts `Transactional<'_>` as a handler parameter,
   which Axum extracts automatically (following sibling patterns).

4. **Error propagation**: uses `.context()` to wrap errors, consistent with
   `common/src/error.rs` patterns. The service method handles 404 internally.

5. **utoipa annotation**: includes OpenAPI path documentation for automatic API
   spec generation, following the project convention for endpoint handlers.

6. **Documentation comment**: the handler function has a `///` doc comment
   describing the endpoint behavior, including the 404 case.

## Convention Adherence

- Follows the handler pattern from `advisory/endpoints/get.rs`:
  - Extract path params via `Path<Id>`
  - Call service method
  - Return `Json(result)`
  - Return type is `Result<Json<T>, AppError>`
- Uses `.context()` error wrapping from `anyhow` / `AppError` pattern.
- Includes `utoipa::path` annotation for OpenAPI spec generation.

## Sibling Comparison

| Aspect | `get.rs` (sibling) | `severity_summary.rs` (new) |
|--------|-------------------|---------------------------|
| Path param | `Path(id): Path<Id>` | `Path(id): Path<Id>` |
| Return type | `Result<Json<AdvisoryDetails>, AppError>` | `Result<Json<SeveritySummary>, AppError>` |
| Service call | `service.fetch(id, &tx)` | `service.severity_summary(id, &tx)` |
| Error handling | `.context(...)` | `.context(...)` |

The new handler mirrors the sibling pattern exactly, substituting only the response
type and service method name.
