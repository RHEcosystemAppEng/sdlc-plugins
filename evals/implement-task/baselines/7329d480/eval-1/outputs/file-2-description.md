# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

New endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that returns severity counts for advisories linked to a given SBOM.

## Detailed Changes

Create a new file with the following contents:

### Imports

```rust
use axum::{extract::Path, Json};
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use trustify_common::db::Transactional;
use trustify_common::id::Id;
```

(Exact import paths would be confirmed by inspecting sibling files like `get.rs` and `list.rs` during Step 4.)

### Handler function

```rust
/// GET handler for /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of unique advisories at each
/// severity level (Critical, High, Medium, Low) and a total count.
pub async fn get(
    service: Extension<AdvisoryService>,  // or State<...> depending on sibling pattern
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to aggregate advisory severity for SBOM")?;

    Ok(Json(summary))
}
```

## Conventions followed

- Follows the endpoint pattern from `advisory/endpoints/get.rs`: extract `Path<Id>`, call service method, return `Json<T>`
- Error handling uses `Result<T, AppError>` with `.context()` wrapping
- Returns 404 implicitly when the service method returns an appropriate error for non-existent SBOMs
- Documentation comment on the handler function
- The exact Axum state extraction mechanism (Extension vs State) would be confirmed from sibling inspection
