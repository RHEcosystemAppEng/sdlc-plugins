# File 4 — CREATE `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

GET handler for `/api/v2/sbom/{id}/advisory-summary`, modelled on `modules/fundamental/src/advisory/endpoints/get.rs` (path extraction via `Path<Id>`, service via the same state/extension extractor, `Result<_, AppError>`, `Json` response).

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::{db::Transactional, error::AppError, id::Id};

use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};

/// Returns per-severity counts of unique advisories affecting the given SBOM.
///
/// Responds `404 Not Found` if the SBOM does not exist.
#[utoipa::path(               // only if sibling handlers carry utoipa annotations
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    tag = "advisory",
    params(("id" = Id, Path, description = "SBOM identifier")),
    responses(
        (status = 200, description = "Advisory severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    )
)]
pub async fn get(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("failed to compute advisory severity summary")?
        .ok_or(AppError::NotFound(format!("SBOM {id} not found")))?;

    Ok(Json(summary))
}
```

Notes:
- The exact state extractor (`State<AdvisoryService>` vs `Extension<...>`), `Transactional` argument and `NotFound` variant shape are copied verbatim from `get.rs` / `sbom/endpoints/get.rs` so 404 behavior is consistent with existing SBOM endpoints.
