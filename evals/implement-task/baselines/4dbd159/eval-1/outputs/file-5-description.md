# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose

Register the new severity summary endpoint route in the advisory module's route table.

## Pre-Implementation Inspection

Before modifying, inspect the file using:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` to see existing route registrations
- Read the file to understand the exact `Router::new().route(...)` chaining pattern

Expected current structure (based on repo structure and conventions):

```rust
mod get;
mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

## Detailed Changes

### Add Module Declaration

Add `mod severity_summary;` to the module declarations at the top:

```rust
mod get;
mod list;
mod severity_summary;
```

### Add Route Registration

Add the new route to the `Router` chain:

```rust
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

### Design Decisions

- **Route path**: `/api/v2/sbom/{id}/advisory-summary` as specified in the API Changes section of the task. The `:id` path parameter syntax follows Axum conventions (may be `{id}` depending on Axum version -- would confirm by inspecting existing routes)
- **Module import**: `mod severity_summary;` follows the alphabetical pattern of existing module declarations
- **Route registration pattern**: Uses the same `Router::new().route("/path", get(handler))` chaining pattern as existing routes
- **Handler reference**: `severity_summary::get_severity_summary` follows the `module::function` reference pattern used by existing routes
- **Placement**: The new route is appended after existing advisory routes in the chain, maintaining logical grouping

### Note on Route Placement

The endpoint path `/api/v2/sbom/{id}/advisory-summary` is under the `/sbom/` path prefix but registered in the advisory module's router. This is architecturally valid because the endpoint's logic lives in the advisory domain (it aggregates advisory data). In a real implementation, I would verify via Serena or code inspection whether this route should instead be registered in the SBOM module's `endpoints/mod.rs`. The task description explicitly says to register it in the advisory module's `endpoints/mod.rs`, so I follow the task specification.
