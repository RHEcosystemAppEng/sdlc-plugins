# File 4 (CREATE): `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

GET handler for `/api/v2/sbom/{id}/advisory-summary`, following `advisory/endpoints/get.rs`:
`Path<Id>` extraction -> service call -> `Json` response, `Result<_, AppError>`.

```rust
use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};
use axum::{extract::{Path, State}, Json};
use trustify_common::{db::Transactional, error::AppError, id::Id};

/// Returns severity counts (critical/high/medium/low/total) of the unique advisories
/// linked to the given SBOM. Responds 404 when the SBOM does not exist.
#[utoipa::path(
    get,
    tag = "advisory",
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(("id" = Id, Path, description = "SBOM identifier")),
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    )
)]
pub async fn severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("failed to compute advisory severity summary")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {id} not found")))?;
    Ok(Json(summary))
}
```

Notes:
- The 404 construction uses exactly the variant/message style found in
  `sbom/endpoints/get.rs` (consistent with existing SBOM endpoints, per AC).
- Extractor style (`State` vs `Extension`) and `utoipa` annotation copied from `get.rs`;
  drop the annotation if siblings don't use it.
