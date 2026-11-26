# File 2 (CREATE): `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Pattern followed: `modules/fundamental/src/advisory/endpoints/get.rs` — extract `Path<Id>`, call
service with `Transactional::None`, map `None` to 404, wrap errors with `.context()`, return JSON.

```rust
use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::{db::Transactional, error::AppError, id::Id};

/// Returns severity counts of unique advisories linked to the given SBOM.
///
/// Responds with 404 when the SBOM does not exist.
#[utoipa::path(
    get,
    tag = "advisory",
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(("id" = Id, Path, description = "SBOM identifier")),
    responses(
        (status = 200, description = "Advisory severity summary for the SBOM", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn get(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id.clone(), &Transactional::None)
        .await
        .context("failed to compute advisory severity summary")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {id} not found")))?;

    Ok(Json(summary))
}
```

Notes:
- Extractor style (`State` vs `Extension`), the `Id` import path, and the exact `AppError::NotFound`
  variant/constructor are copied verbatim from `advisory/endpoints/get.rs` / `sbom/endpoints/get.rs`
  after inspecting them with `find_symbol(include_body=true)`; the snippet shows the intended shape.
- `.context()` import comes from the same place siblings import it (`anyhow::Context` or the
  common error extension trait in `common/src/error.rs`).
- `#[utoipa::path]` is included only if sibling handlers carry it.
