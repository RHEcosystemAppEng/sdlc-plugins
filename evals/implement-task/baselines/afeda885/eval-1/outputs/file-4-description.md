# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from path parameters, calls the service method, and returns the JSON response.

## Detailed Changes

Create a new file with the following contents:

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use common::error::AppError;
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};

/// GET handler for `/api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
/// Responds with a JSON `SeveritySummary` containing critical, high, medium, low,
/// and total counts. Returns 404 if the SBOM ID does not exist.
pub async fn get_advisory_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await?;
    Ok(Json(summary))
}
```

## Conventions Applied

- **Endpoint pattern**: Follows the existing pattern in `endpoints/get.rs` -- extract path params via `Path<Id>`, call service, return JSON
- **File naming**: Named `severity_summary.rs` matching the action/resource naming convention used for endpoint files
- **Error handling**: Returns `Result<T, AppError>` -- errors from the service layer propagate automatically via the `?` operator
- **Response type**: Returns the struct directly via Axum's `Json` extractor for automatic serialization (as specified in Implementation Notes)
- **State extraction**: Uses Axum's `State` extractor to access the `AdvisoryService` (matching sibling endpoint patterns)
- **Documentation**: Doc comment on the handler function explaining the endpoint, response shape, and error behavior
- **Minimal handler logic**: The handler delegates all business logic to the service layer, keeping the endpoint thin (consistent with sibling handlers)
