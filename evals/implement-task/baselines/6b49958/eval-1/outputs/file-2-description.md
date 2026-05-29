# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM.

## Detailed Changes

Create a new file with the following contents:

### Imports

```rust
use actix_web::HttpResponse;  // or axum equivalents depending on framework
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use trustify_common::error::AppError;
use trustify_common::db::Transactional;
use trustify_common::id::Id;
```

Note: The exact import paths will be confirmed by inspecting `get.rs` at implementation time. The pattern above mirrors what the existing `get.rs` handler uses.

### Handler Function

```rust
/// Retrieve aggregated advisory severity counts for a specific SBOM.
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
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await?
        .ok_or_else(|| AppError::not_found("SBOM not found".to_string()))
        .context("fetching severity summary for SBOM")?;

    Ok(Json(summary))
}
```

### Design Decisions

- **`Path<Id>` extraction:** Follows the exact pattern from `get.rs` for extracting the SBOM identifier from the URL path.
- **`State<AdvisoryService>`:** The service is injected via Axum's `State` extractor, matching the existing endpoint pattern.
- **`Transactional<'_>`:** Transaction context is extracted from the request, following the established pattern.
- **`Result<Json<SeveritySummary>, AppError>`:** Standard return type matching all existing handlers.
- **404 handling:** When the service method returns `None` (SBOM not found), it is converted to `AppError::not_found`, consistent with existing SBOM endpoints.
- **`.context()` wrapping:** Error context is added following the `common/src/error.rs` pattern.
- **`#[utoipa::path]` annotation:** OpenAPI documentation is generated automatically, following the convention seen in existing endpoint handlers.

### Notes on Framework Detection

The exact Axum vs Actix-web imports and extractor patterns will be finalized by reading `get.rs` at implementation time. The task description references `Path<Id>` and `Json` which are Axum patterns, so the plan assumes Axum. If the project uses Actix-web, the handler signature would use `web::Path<Id>` and `web::Json<T>` instead, but the logic remains identical.
