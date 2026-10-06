# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts
the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method,
and returns the result as JSON.

## Pre-implementation inspection

Before creating, inspect sibling endpoint handlers:
```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/get.rs")
mcp__serena_backend__find_symbol("get_advisory", include_body=true)
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/sbom/endpoints/get.rs")
```

Understand:
- How `Path<Id>` is extracted
- How the service is accessed (Axum State, Extension, or function parameter)
- How errors are propagated
- How JSON responses are returned

## Content

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
// Additional imports based on how service/tx are injected in siblings

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// with counts per severity level (critical, high, medium, low) and a total.
pub async fn get_advisory_summary(
    Path(sbom_id): Path<Id>,
    service: /* injected via Axum -- match sibling pattern (State, Extension, etc.) */,
    tx: /* transaction context -- match sibling pattern */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("failed to aggregate advisory severity for SBOM")?;

    Ok(Json(summary))
}
```

The exact injection mechanism (State, Extension, or function parameters) will be
determined by reading the sibling `get.rs` handler. The pattern will be replicated
exactly.

## Design decisions

- **Path extraction**: `Path<Id>` matches the pattern in `get.rs` per Implementation Notes
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping matches convention
- **Response type**: Return `Json<SeveritySummary>` directly -- Axum handles serialization
- **Doc comment**: Handler has a doc comment explaining the endpoint per skill guidance
- **No pagination**: This is a summary endpoint returning a single aggregate object, not a list -- no need for `PaginatedResults<T>`

## Convention conformance

- Handler function signature matches sibling endpoint handlers in `get.rs` and `list.rs`
- Import organization: axum imports, then crate-local imports, then common imports
- Error wrapping uses `.context()` with a descriptive message
- Return type wraps model in `Json<T>`
