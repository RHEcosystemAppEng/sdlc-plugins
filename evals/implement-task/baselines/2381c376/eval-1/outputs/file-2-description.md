# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Operation: CREATE

## Purpose

Define the Axum GET handler for `GET /api/v2/sbom/{id}/advisory-summary`. Extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` as JSON.

## Sibling Reference

Follows the endpoint handler pattern in `modules/fundamental/src/advisory/endpoints/get.rs` for path parameter extraction, service invocation, error handling, and response serialization.

## Detailed Changes

### Imports

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
use trustify_common::db::Transactional;
```

(Exact import paths would be confirmed by inspecting sibling `get.rs` imports via Serena `get_symbols_overview`.)

### Handler Function

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM. Deduplicates advisories by ID before counting.
pub async fn get_advisory_severity_summary(
    Path(sbom_id): Path<Id>,
    service: AdvisoryService,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &Transactional::None)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Function name**: `get_advisory_severity_summary` follows the `verb_noun` naming convention discovered in sibling analysis.
- **Path extraction**: `Path(sbom_id): Path<Id>` matches the pattern in `get.rs` for extracting path parameters.
- **Service injection**: `AdvisoryService` is injected as an Axum extractor (via `FromRequestParts` or state), matching the existing endpoint pattern.
- **Transactional**: Uses `Transactional::None` for read-only queries, consistent with GET endpoints.
- **Error handling**: `.context()` wrapping on the service call, returning `Result<T, AppError>`, matching the established error handling pattern.
- **Response**: Returns `Json<SeveritySummary>` directly -- Axum handles serialization.
- **Doc comment**: Documents the handler's purpose, matching skill guidance for all new public functions.

## Conventions Applied

- snake_case function name with `get_` prefix for GET handlers
- `Path<Id>` extraction pattern from sibling `get.rs`
- `Result<Json<T>, AppError>` return type
- `.context()` error wrapping
- Single responsibility -- handler delegates to service, does not contain business logic
