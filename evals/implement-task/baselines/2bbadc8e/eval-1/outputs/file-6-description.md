# File 6: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: Create (new file)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the JSON response.

## Full File Content

```rust
//! GET handler for SBOM advisory severity summary.
//!
//! Returns aggregated advisory severity counts for a given SBOM ID.

use actix_web::web;
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Retrieve aggregated advisory severity counts for a specific SBOM.
///
/// Returns a JSON object with counts per severity level (critical, high,
/// medium, low) and a total count of unique advisories linked to the SBOM.
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to get severity summary")?;

    Ok(Json(summary))
}
```

## Rationale

- **Path extraction**: Uses `Path<Id>` to extract the SBOM ID from the URL path parameter, following the pattern in `advisory/endpoints/get.rs`
- **Service injection**: Uses `State<AdvisoryService>` extractor, matching the existing endpoint pattern for service access
- **Transactional context**: Takes `Transactional<'_>` for database operations, matching the service method signature
- **Response type**: Returns `Result<Json<SeveritySummary>, AppError>` -- Axum's `Json` wrapper handles serialization, `AppError` handles error responses
- **Error handling**: Uses `.context()` for error wrapping per project convention
- **Documentation**: Public function has a doc comment explaining its behavior, parameters, and error responses per skill guidance

## Convention Conformance

- Handler function naming: `get_severity_summary` follows `verb_noun` pattern (cf. `get_by_id` in `get.rs`)
- One handler per file (cf. `list.rs`, `get.rs`)
- Return type: `Result<Json<T>, AppError>` matches sibling endpoints
- Extractor usage: `Path`, `State`, `Transactional` matches sibling handler signatures
- Import organization: external crates first, then internal modules

## Defensive Property Access

- The service layer handles null/missing SBOM by returning a 404 AppError
- Severity string matching uses `unwrap_or_default()` to handle null severity fields
- The `SeveritySummary` struct defaults all fields to 0, so missing severity levels are safe
