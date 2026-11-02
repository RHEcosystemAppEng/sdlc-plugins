# File 5 — Create: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## What changes

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

## Code inspection

Before creating, inspect `advisory/endpoints/get.rs` with `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol(name_path_pattern="get")` with `include_body=true` to understand the handler pattern: path param extraction via `Path<Id>`, service call, JSON response.

## Detailed changes

```rust
use crate::advisory::{model::severity_summary::SeveritySummary, service::AdvisoryService};
use actix_web::web;
use axum::{
    extract::{Path, State},
    Json,
};
use common::error::AppError;
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// GET handler for /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn get(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await?;
    Ok(Json(summary))
}
```

## Patterns followed

- Follows `advisory/endpoints/get.rs` pattern exactly: extract `Path<Id>`, call service, return `Json<T>`
- Uses `State(service)` for service injection (Axum pattern)
- Error handling via `Result<T, AppError>` — errors propagate via `?` operator
- OpenAPI documentation via `utoipa::path` attribute
- Returns the struct directly; Axum's `Json` extractor handles serialization
