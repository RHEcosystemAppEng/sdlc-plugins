# File 4 (CREATE): `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

GET handler for `/api/v2/sbom/{id}/advisory-summary`.
Pattern source: `modules/fundamental/src/advisory/endpoints/get.rs` — `Path<Id>` extraction, service call, JSON response, `Result<_, AppError>`.

```rust
use axum::{extract::{Path, State}, Json};
use trustify_common::{db::Transactional, error::AppError, id::Id};

use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};

/// Returns counts of unique advisories per severity level for the given SBOM.
///
/// Responds with 404 when the SBOM does not exist.
#[utoipa::path(
    get,
    tag = "advisory",
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(("id" = Id, Path, description = "SBOM identifier")),
    responses(
        (status = 200, description = "Advisory severity counts for the SBOM", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await?;
    Ok(Json(summary))
}
```

Notes:
- State extraction (`State<AdvisoryService>` vs `Extension<...>`), transaction argument, and import paths are copied verbatim from `get.rs`.
- The `#[utoipa::path]` annotation is only kept if `get.rs` uses it; if so, the handler must also be added to the module's OpenAPI path list wherever siblings are listed (within `endpoints/mod.rs`).
- Errors from the service already carry `.context()`; the handler propagates with `?` exactly like `get.rs`.
