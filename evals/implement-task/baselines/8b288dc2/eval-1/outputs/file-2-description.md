# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

**Action**: Create new file

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` as JSON.

## Conventions Applied

- **Handler pattern**: Follows `modules/fundamental/src/advisory/endpoints/get.rs` -- extract path params via `Path<Id>`, call service, return `Json`.
- **Error handling**: Returns `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping, matching `common/src/error.rs` pattern.
- **Function naming**: Named `severity_summary` following the verb-free handler naming in sibling files (e.g., `get` in `get.rs`, `list` in `list.rs`).
- **Documentation**: Doc comment on the handler function.

## Detailed Changes

```rust
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all unique advisories linked to the
/// specified SBOM. Returns 404 if the SBOM ID does not exist.
pub async fn severity_summary(
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

## Design Decisions

- **`Path<Id>` extraction**: Matches the existing `get.rs` handler pattern exactly. The `Id` type is the shared identifier type from `common`.
- **`State<AdvisoryService>`**: Extracts the service from Axum application state, following the dependency injection pattern used by sibling handlers.
- **`Transactional` parameter**: Matches the signature pattern in `AdvisoryService::fetch` and `AdvisoryService::list`.
- **Error wrapping with `.context()`**: Provides a descriptive error message for debugging while letting `AppError`'s `IntoResponse` implementation handle HTTP status code mapping (404 for not-found, 500 for internal errors).
- **No explicit 404 logic in handler**: The 404 for non-existent SBOM IDs is handled inside the service method (consistent with how `fetch` handles missing entities), which returns an appropriate `AppError` variant that maps to HTTP 404.
