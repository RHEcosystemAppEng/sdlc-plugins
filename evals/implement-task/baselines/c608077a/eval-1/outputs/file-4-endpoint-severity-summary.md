# File 4 — CREATE `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

GET handler for `/api/v2/sbom/{id}/advisory-summary`, modeled on `modules/fundamental/src/advisory/endpoints/get.rs` (same extractor style, service access, error type, OpenAPI annotation).

```rust
use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::{db::Transactional, error::AppError, id::Id};

/// Returns per-severity counts of unique advisories affecting an SBOM.
///
/// Responds with 404 if the SBOM does not exist.
#[utoipa::path(
    get,
    tag = "advisory",
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Advisory severity summary for the SBOM", body = SeveritySummary),
        (status = 404, description = "The SBOM could not be found"),
    ),
)]
pub async fn severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

Notes:
- `State` vs `Extension` and import paths (`trustify_common::...`) mirror exactly what `get.rs` uses (confirmed via `find_symbol` on `get`).
- NotFound from the service propagates through `AppError` -> 404, as in the SBOM `get` endpoint.
- If `get.rs` attaches cache headers via the tower-http layer in the route builder, the same is applied in `mod.rs` (file 5), not here.
