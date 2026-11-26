# File 4 (CREATE): `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose
This file holds the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

## Pattern source
`modules/fundamental/src/advisory/endpoints/get.rs`: extract `Path<Id>`, call the service, return
JSON, and return `Result<_, AppError>` with `.context()`. Read with
`mcp__serena_backend__find_symbol("get", relative_path="modules/fundamental/src/advisory/endpoints/get.rs", include_body=true)`
before writing, so the extractor types (`State` vs `Extension`), the DB/transaction acquisition and
the `utoipa::path` annotation match exactly.

## Content

```rust
use axum::{extract::{Path, State}, Json};
use trustify_common::{db::Transactional, error::AppError, id::Id};

use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};

/// Returns the counts of unique advisories per severity level for an SBOM.
///
/// Responds with 404 when the SBOM does not exist, matching `GET /api/v2/sbom/{id}`.
#[utoipa::path(
    get,
    tag = "advisory",
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(("id" = Id, Path, description = "SBOM identifier")),
    responses(
        (status = 200, description = "Advisory severity summary for the SBOM", body = SeveritySummary),
        (status = 404, description = "The SBOM could not be found"),
    ),
)]
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id.clone(), &Transactional::None)
        .await
        .context(format!("Failed to compute advisory severity summary for SBOM {id}"))?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {id} not found")))?;

    Ok(Json(summary))
}
```

## Notes
- The 404 path uses the same `AppError` not-found variant as `sbom/endpoints/get.rs`, so the
  response body format matches existing SBOM endpoints (acceptance criterion 2). Confirm the
  variant name in `common/src/error.rs` before writing.
- The response is the `SeveritySummary` struct serialized through `Json`, with no
  `PaginatedResults` wrapper because this is not a list endpoint.
- The handler name `get_severity_summary` follows the `get`/`list` handler naming in sibling files.
  If siblings name handlers just `get`/`list`, use `severity_summary` instead.
