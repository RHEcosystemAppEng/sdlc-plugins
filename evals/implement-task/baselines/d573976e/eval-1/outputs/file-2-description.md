# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that retrieves severity counts for advisories linked to a given SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use actix_web::{web, HttpResponse};
use axum::extract::{Path, State};
use axum::Json;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts (critical, high, medium, low, total)
/// for all unique advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Followed

- **Endpoint pattern**: follows the exact pattern from `modules/fundamental/src/advisory/endpoints/get.rs` — extracts path params via `Path<Id>`, calls service method, returns `Json<T>`.
- **Error handling**: returns `Result<T, AppError>` with `.context()` wrapping, matching the pattern in `common/src/error.rs` and all other endpoint handlers.
- **Response type**: returns the struct directly via Axum's `Json` extractor for automatic serialization.
- **Documentation**: doc comment on the handler function explaining the endpoint's behavior.
- **Naming**: file named `severity_summary.rs` matching the operation name, consistent with `get.rs`, `list.rs` naming in the same directory.
