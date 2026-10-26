# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM.

## Pre-Implementation Inspection

Before creating, would:
1. `mcp__serena_backend__get_symbols_overview` on `endpoints/get.rs` (advisory) to understand the exact handler signature pattern, imports, and service access pattern
2. `mcp__serena_backend__find_symbol` with `include_body=true` on the `get` handler in `endpoints/get.rs` to see the full implementation pattern
3. `mcp__serena_backend__get_symbols_overview` on `../sbom/endpoints/get.rs` to see how SBOM-scoped handlers extract the SBOM ID path parameter
4. Check how `AppError` is imported and how 404 errors are constructed from service-level errors

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
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// with counts per severity level (Critical, High, Medium, Low) and a total.
pub async fn severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .map_err(AppError::from)?;

    Ok(Json(summary))
}
```

## Notes

- **Handler signature:** Follows the exact pattern from sibling `get.rs` -- `Path<Id>` for path parameter extraction, `State<AdvisoryService>` for service access (or whatever mechanism siblings use -- could be `Extension` instead of `State` depending on Axum version). Would verify by reading the sibling handler.
- **Transaction parameter:** Uses `Transactional::None` as the default, matching the pattern in existing handlers. If siblings use a different transaction strategy (e.g., read-only transactions from middleware), would match that pattern.
- **Error handling:** Converts service errors to `AppError` using `.map_err(AppError::from)` or `.context()` wrapping, depending on the sibling pattern. The service method already wraps errors with `.context()`, so the handler can propagate them directly.
- **404 handling:** The service method checks SBOM existence and returns an error if not found. The `AppError` conversion maps this to an HTTP 404 response. Would verify the exact error mapping by inspecting `common/src/error.rs` to ensure `anyhow::Error` containing "not found" text maps to 404, or if a specific error variant is needed.
- **Import paths:** The exact import paths (`common::error::AppError`, `trustify_common::db::Transactional`, etc.) depend on the project's crate structure. Would verify by inspecting sibling handler imports. The import for `Id` might be `trustify_common::id::Id` or a local re-export.
- **No caching:** The task does not mention caching requirements. If sibling endpoints use `tower-http` caching middleware configuration, would evaluate whether to add it, but since the task is silent on this, would omit and flag as a potential follow-up.
