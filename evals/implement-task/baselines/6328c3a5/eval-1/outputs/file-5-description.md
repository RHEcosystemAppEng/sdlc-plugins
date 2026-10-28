# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Pre-implementation Inspection

Before creating, would inspect sibling endpoint files for convention conformance:

1. `mcp__serena_backend__find_symbol(name_path_pattern="advisory::endpoints::get", include_body=true)` -- read the GET handler in `get.rs` for the exact pattern (path extraction, service call, error handling, response type)
2. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/list.rs")` -- compare list handler pattern
3. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/sbom/endpoints/get.rs")` -- cross-module comparison for SBOM-specific endpoint patterns

## File Content

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
// Additional imports as needed based on inspection (e.g., Id type, Transactional, State)

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
/// Responds with 404 if the SBOM ID does not exist.
pub async fn get_severity_summary(
    Path(sbom_id): Path<Id>,
    // State or Extension extractor for AdvisoryService, matching sibling pattern
    // e.g., State(service): State<AdvisoryService> or Extension(service): Extension<AdvisoryService>
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &Transactional::None)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Handler signature**: Follows the exact pattern from `advisory/endpoints/get.rs`:
  - `Path<Id>` for SBOM ID extraction from URL path
  - Service injected via Axum's state/extension mechanism (exact method determined by sibling inspection)
  - Returns `Result<Json<T>, AppError>`

- **Error handling**: Uses `.context()` wrapping on the service call, matching the error handling pattern in `common/src/error.rs` and sibling handlers. The `AppError` type implements `IntoResponse`, so Axum automatically converts errors to appropriate HTTP responses (including 404).

- **Transactional context**: Passes `&Transactional::None` (or the appropriate transactional context from the handler's scope), matching how sibling handlers invoke service methods.

- **Response type**: Returns `Json<SeveritySummary>` directly -- Axum serializes via serde. No manual `serde_json::to_string` or response building needed.

- **Documentation**: The handler function has a `///` doc comment explaining what it does and its error behavior.

## Convention conformance

- Function name: `get_severity_summary` -- uses `verb_noun` pattern matching `get_advisory`, `list_advisories`
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Path extraction: `Path<Id>` matching sibling GET handlers
- Response: direct struct return via `Json<T>`, matching sibling pattern
- No manual status code construction -- relies on Axum's `IntoResponse` implementations

## Defensive property access

The handler delegates all data processing to the service layer. No direct property access on external data in the handler itself. Defensive access is handled in the service method (file-1-description.md).
