# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns
aggregated advisory severity counts for a given SBOM.

## Detailed Changes

### Handler function

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// Queries all advisories linked to the given SBOM via the `sbom_advisory` join table,
/// deduplicates by advisory ID, and returns counts per severity level.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design decisions

- **Pattern follows `get.rs`**: the existing `get.rs` handler in the same directory
  extracts `Path<Id>`, calls a service method, and returns `Json(result)`. This handler
  follows the identical pattern.
- **Error handling with `.context()`**: wraps the service call error with a descriptive
  message, matching the convention in `common/src/error.rs` and all sibling handlers.
- **`Extension` extractors**: uses Axum's `Extension` for dependency injection of the
  service and transactional context, matching sibling endpoint patterns.
- **Return type `Result<Json<SeveritySummary>, AppError>`**: follows the standard
  handler return type convention.

### Conventions followed

- Handler file named after the operation: `severity_summary.rs` (matches `get.rs`, `list.rs`).
- Single public async function per handler file.
- Doc comment on the public function explaining what it does.
- Error wrapping with `.context()`.
