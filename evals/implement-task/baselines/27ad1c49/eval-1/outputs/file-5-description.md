# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts.

## Pre-Implementation Inspection

1. `mcp__serena_backend__find_symbol` on the handler function in `modules/fundamental/src/advisory/endpoints/get.rs` with `include_body=true` to see the complete handler pattern:
   - Path parameter extraction via `Path<Id>`
   - Service instantiation or injection pattern
   - Service method call with transaction
   - JSON response wrapping
   - Error handling with `AppError`
2. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` to cross-reference handler patterns across domains.
3. Check how `Transactional` is obtained in handlers (from request extensions, middleware, or explicit creation).

## File Contents

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional; // or wherever Transactional is imported from

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// with counts per severity level (Critical, High, Medium, Low) and a total.
pub async fn get_severity_summary(
    Path(sbom_id): Path<Id>,
    service: /* injected AdvisoryService -- match sibling pattern (Extension, State, or similar) */,
    tx: /* Transactional extraction -- match sibling pattern */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

### Implementation Notes

- The exact handler signature depends on how the existing `get.rs` handler in the advisory module extracts its dependencies. The sibling pattern must be followed exactly:
  - If services are injected via `Extension<AdvisoryService>`, use the same pattern
  - If services are accessed via `State<AppState>`, follow that pattern
  - If `Transactional` is obtained from a middleware extension, match that extraction
- The path parameter type (`Id`) should match the type used in sibling handlers for consistency
- Error context string follows the `"failed to <action>"` pattern observed in siblings
- The handler function name `get_severity_summary` follows the verb_noun convention

### Cross-Repo API Contract Verification

Since this is a new endpoint (not calling another service), verify:
1. The path `/api/v2/sbom/{id}/advisory-summary` is consistent with the API Changes section
2. The response shape `{ critical, high, medium, low, total }` matches the API Changes specification
3. The HTTP method (GET) matches the specification

## Convention Compliance

- Handler returns `Result<Json<T>, AppError>` matching all sibling handlers
- Path extraction via `Path<Id>` matching `get.rs` pattern
- Error wrapping with `.context()` matching established pattern
- Documentation comment on the handler function
- Import organization: external crates first, internal crates second, local modules last
