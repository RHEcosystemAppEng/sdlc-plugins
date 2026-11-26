# File 4 — CREATE `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

**Purpose**: the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

**Pattern followed**: `advisory/endpoints/get.rs`, read with `find_symbol(include_body=true)` first. The
extractor set, service injection mechanism, `#[utoipa::path]` / tracing attributes, and return
type are copied exactly from it.

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::{db::Transactional, error::AppError, id::Id};

use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};

/// Returns per-severity counts of the unique advisories linked to an SBOM.
///
/// `GET /api/v2/sbom/{id}/advisory-summary` responds with
/// `{ critical, high, medium, low, total }`, or 404 if the SBOM does not exist.
#[utoipa::path(
    get,
    tag = "advisory",
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(("id" = Id, Path, description = "SBOM identifier")),
    responses(
        (status = 200, description = "Advisory severity counts for the SBOM", body = SeveritySummary),
        (status = 404, description = "The SBOM was not found"),
    )
)]
pub async fn get_severity_summary(
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
- Keep the `#[utoipa::path]` attribute only if `get.rs` uses it, and match its `tag` value.
- If `get.rs` injects the service with `Extension<Arc<AdvisoryService>>` or a shared `AppState`, use the same mechanism.
- The service already maps a missing SBOM to `AppError::NotFound`. Check during inspection that `.context()` on `AppError` keeps the variant (and so the 404). If it does not, drop the extra `.context()` here, as `get.rs` does.
