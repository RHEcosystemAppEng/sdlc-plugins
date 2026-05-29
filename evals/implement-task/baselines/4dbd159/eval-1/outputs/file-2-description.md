# File 2: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Detailed Changes

Create a new file with the following content:

### Imports

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use common::db::Transactional;
```

Following the import pattern from sibling `get.rs` endpoint file.

### Handler Function

```rust
/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// Queries all advisories linked to the given SBOM via the sbom_advisory join table,
/// deduplicates by advisory ID, and returns counts grouped by severity level.
/// Returns 404 if the SBOM ID does not exist.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier")
    ),
    responses(
        (status = 200, description = "Advisory severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found")
    )
)]
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: AdvisoryService,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design Decisions

- **Parameter extraction pattern**: Uses `Path<Id>` exactly like sibling `get.rs`
- **Service call pattern**: Calls service method passing `id` and `&tx`, matching the established `fetch` / `list` pattern
- **Error handling**: Uses `.context()` wrapping to produce descriptive `AppError`, matching sibling handlers
- **Return type**: `Result<Json<SeveritySummary>, AppError>` following the handler return convention
- **404 handling**: The service method itself will return an error when the SBOM ID doesn't exist; `AppError` converts this to a 404 response (consistent with existing SBOM endpoints)
- **utoipa annotation**: Follows the OpenAPI documentation pattern from sibling endpoints for auto-generated API docs
- **Doc comment**: Describes what the handler does, per Step 6 code quality requirements
