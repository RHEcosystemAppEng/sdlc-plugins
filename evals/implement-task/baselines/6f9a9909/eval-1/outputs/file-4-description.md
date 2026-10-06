# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

HTTP GET handler for `/api/v2/sbom/{id}/advisory-summary` that delegates to
`AdvisoryService::severity_summary` and returns the result as JSON.

## Content

```rust
use axum::{
    extract::Path,
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity breakdown (critical, high, medium, low, total) of
/// advisories linked to the specified SBOM.
pub async fn get(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService state */,
    tx: /* injected Transactional */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Implementation Details

### Handler Signature

The exact signature follows the pattern in the sibling `get.rs` endpoint handler:
- `Path<Id>` extractor for the SBOM ID from the URL path
- Service and transaction state injected via Axum extractors (the exact mechanism
  depends on how the project wires state -- likely `Extension<AdvisoryService>` or
  a custom extractor)
- Returns `Result<Json<SeveritySummary>, AppError>`

### Error Handling

- `.context("fetching advisory severity summary")` wrapping follows the established
  pattern from `common/src/error.rs`
- 404 errors from the service layer propagate naturally through the `?` operator
- `AppError` implements `IntoResponse`, so Axum converts it to the appropriate HTTP status

### Response Format

The `Json` extractor serializes `SeveritySummary` to:

```json
{
  "critical": 3,
  "high": 12,
  "medium": 7,
  "low": 2,
  "total": 24
}
```

## Conventions Applied

- File naming: `severity_summary.rs` matching the domain action
- Handler function named `get` matching sibling `get.rs` convention
- Extracts path params via `Path<Id>`, calls service, returns JSON -- exact pattern
  from `modules/fundamental/src/advisory/endpoints/get.rs`
- Error handling with `.context()` wrapping
- Doc comment on the handler function
