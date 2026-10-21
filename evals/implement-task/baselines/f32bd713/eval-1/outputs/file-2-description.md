# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: Create

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This endpoint receives
an SBOM ID as a path parameter, calls `AdvisoryService::severity_summary`, and returns the
aggregated severity counts as JSON.

## Pre-implementation inspection

Before creating this file, would inspect siblings using Serena:

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand the existing GET handler pattern (imports, function signature, error handling, response type)
- `mcp__serena_backend__find_symbol` with `include_body=true` on the `get` handler function in `advisory/endpoints/get.rs` -- read the full implementation to replicate the pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-reference with another domain's GET handler for consistency
- `mcp__serena_backend__find_symbol` with `include_body=true` on `Path` extractor usage -- understand how path params are extracted
- `mcp__serena_backend__search_for_pattern` for `AppError` usage in endpoint handlers -- understand error wrapping pattern
- `mcp__serena_backend__find_symbol` on `Id` type -- confirm the type used for entity identifiers

## Detailed changes

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::id::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// broken down by severity level (critical, high, medium, low) with a total.
pub async fn severity_summary(
    service: AdvisoryService,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = service.db.transaction().await?;
    let summary = service
        .severity_summary(&id, &tx)
        .await
        .context("failed to aggregate advisory severities")?;
    Ok(Json(summary))
}
```

## Conventions applied

- Path parameter extracted via `Path<Id>`, matching the pattern in `advisory/endpoints/get.rs`
- Returns `Result<Json<SeveritySummary>, AppError>`, matching the `Result<T, AppError>` convention
- Error wrapped with `.context()` for descriptive error messages, matching `common/src/error.rs` pattern
- Struct returned directly via `Json` extractor (Axum handles serialization)
- `///` doc comment on the handler function describing what it does
- Import organization: axum first, internal crate modules second
- Function name `severity_summary` follows snake_case verb_noun convention (though here noun acts as the descriptor)
- Defensive: transaction acquired at handler level, matching sibling handler patterns

## Notes

- The exact import paths and type names would be confirmed by Serena inspection of siblings
- The transaction pattern (`service.db.transaction()`) would be verified against the existing `get.rs` handler
- If the sibling pattern uses a different service injection style (e.g., `State` extractor vs function parameter), would match that style
