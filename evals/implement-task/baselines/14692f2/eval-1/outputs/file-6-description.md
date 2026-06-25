# File 6: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Purpose
Register the new severity summary route in the advisory endpoints module so that `GET /api/v2/sbom/{id}/advisory-summary` is served by the new handler.

## Detailed Changes

### New Import
Add import for the severity summary handler module:

```rust
mod severity_summary;
```

And import the handler function:

```rust
use severity_summary::get_advisory_summary;
```

### Route Registration
Add a new `.route()` call to the existing `Router::new()` chain in the route registration function. Following the existing pattern of `Router::new().route("/path", get(handler))`:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(get_advisory_summary))
```

This should be added alongside the existing route registrations in the `mod.rs` file's router builder.

### Expected State After Modification

The router builder will look approximately like:

```rust
Router::new()
    // ... existing advisory routes ...
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

### Design Note
The endpoint path `/api/v2/sbom/{id}/advisory-summary` is scoped under the SBOM path (not the advisory path) because it returns advisory data for a specific SBOM. This is a cross-entity endpoint that lives in the advisory module because the business logic (severity aggregation) is an advisory concern, but the URL is SBOM-centric because the consumer queries by SBOM ID. This pattern is consistent with how join-table queries work — the advisory module owns the aggregation logic while the URL reflects the SBOM context.

## Conventions Applied
- **Route registration**: `Router::new().route("/path", get(handler))` pattern matching existing routes in sibling endpoint `mod.rs` files
- **Module declaration**: `mod severity_summary;` following existing handler module pattern
- **HTTP method**: `get()` for read-only data retrieval
- **Path parameter syntax**: Uses Axum's `:id` syntax for path parameters
