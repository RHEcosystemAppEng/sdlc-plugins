# File 5: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Inspection performed

Used `mcp__serena_backend__find_symbol` with `include_body=true` on the handler functions in sibling endpoint files to understand the full implementation pattern:
- `modules/fundamental/src/advisory/endpoints/get.rs` -- `get_advisory` handler: extracts `Path(id)`, calls `service.fetch(id, &tx)`, returns `Json(result)` or `AppError::NotFound`
- `modules/fundamental/src/advisory/endpoints/list.rs` -- `list_advisories` handler: extracts query params, calls `service.list(...)`, returns `Json(PaginatedResults)`
- `modules/fundamental/src/sbom/endpoints/get.rs` -- `get_sbom` handler: same pattern for SBOM entity

Also used `mcp__serena_backend__find_referencing_symbols` on the handlers to see how they are wired into the router.

## File content

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
/// Returns a severity summary with counts of unique advisories at each severity
/// level (Critical, High, Medium, Low) linked to the specified SBOM, along with
/// a total count.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = Transactional::new_read_only();
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to get severity summary")?;

    Ok(Json(summary))
}
```

## Rationale

- **Handler signature**: Follows the exact pattern from `get.rs` -- `async fn`, `State` for service injection, `Path<Id>` for path parameter extraction, `Result<Json<T>, AppError>` return type
- **Error handling**: Uses `.context()` wrapping consistent with all sibling handlers
- **Transaction**: Uses a read-only transaction since this is a query-only operation
- **Doc comment**: Includes `///` doc comment describing what the endpoint does, per code quality requirements
- **Import organization**: Standard library first, external crates second, internal crates third -- matching the convention discovered in sibling files
