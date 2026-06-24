# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: Create (new file)

## Pre-Implementation Inspection

Before creating, inspect the sibling endpoint file for exact pattern conformance:
- `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function in `modules/fundamental/src/advisory/endpoints/get.rs` to see the exact pattern for path parameter extraction, service invocation, and JSON response return
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` to cross-check the pattern is consistent across modules
- `mcp__serena_backend__find_referencing_symbols` on `AppError` to confirm error handling patterns

## File Contents

Create the GET handler for `/api/v2/sbom/{id}/advisory-summary`:

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

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design Decisions

- Follows the exact pattern from `advisory/endpoints/get.rs`: extract `Path<Id>`, call service method, return `Json<T>`
- Error handling uses `.context()` wrapping per `common/src/error.rs` conventions
- The handler function name follows the `get_<resource>` pattern observed in sibling endpoints
- Doc comment on the public function explains what the handler does
- Imports follow the same organization pattern as sibling endpoint files (axum extracts first, then internal modules, then common)

### Notes

- The exact import paths and State extractor usage will be confirmed by reading `get.rs` -- the skeleton above is based on the described patterns and will be adjusted to match the precise conventions found in the codebase
- If the existing endpoints use a different transaction passing mechanism (e.g., extension instead of extractor), the handler will be adjusted accordingly
