# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Purpose
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service method, and returns the severity summary as JSON.

## Detailed Changes

Create a new file with the following content:

### Imports
- `axum::extract::Path` — for extracting the SBOM ID from the URL path
- `axum::Json` — for JSON response serialization
- The project's `Id` type used for entity identifiers
- `AdvisoryService` from `../../service/advisory`
- `SeveritySummary` from `../../model/severity_summary`
- `AppError` from `common/src/error` — for error handling
- `Transactional` / database connection types as used by sibling handlers

### Handler Function

```rust
/// Retrieves aggregated advisory severity counts for a given SBOM.
///
/// Returns a JSON object with counts per severity level (critical, high,
/// medium, low) and a total count of unique advisories linked to the SBOM.
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_advisory_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(&id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

### Pattern Details
- **Path extraction**: Uses `Path<Id>` following the existing pattern in `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs`
- **Service call**: Calls `service.severity_summary(&id, &tx)` following the same pattern as `service.fetch()` and `service.list()`
- **Error handling**: Uses `Result<T, AppError>` with `.context()` wrapping, matching the pattern in `common/src/error.rs`
- **Response type**: Returns struct directly via `Json<SeveritySummary>` — Axum handles serialization
- **404 handling**: The service method returns an appropriate `AppError` when the SBOM ID is not found, consistent with existing SBOM endpoints

## Conventions Applied
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Path params**: `Path<Id>` extractor following sibling handlers
- **Return type**: Direct `Json<T>` response (not `PaginatedResults` since this is a single aggregate, not a list)
- **Documentation**: Doc comment on the handler function explaining what it does, the response shape, and error behavior
