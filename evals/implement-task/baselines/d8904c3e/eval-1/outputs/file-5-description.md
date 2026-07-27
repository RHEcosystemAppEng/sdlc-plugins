# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary route in the advisory endpoints module so it is accessible via HTTP.

## Current State

The file currently registers routes for listing and getting advisories:

```rust
pub mod get;
pub mod list;

// Route registration function (conceptual):
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

## Changes

### 1. Add module declaration

Add the new submodule declaration:

```rust
pub mod get;
pub mod list;
pub mod severity_summary;
```

### 2. Register the new route

Add the severity summary route to the router registration. The endpoint path is under `/api/v2/sbom/{id}/advisory-summary` (not under `/api/v2/advisory`), as specified in the task description:

```rust
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::severity_summary),
        )
}
```

### Design Decisions

- **Route path**: The endpoint is under `/api/v2/sbom/{id}/advisory-summary` as specified in the task. Although this handler is in the advisory module, the route references an SBOM ID because the endpoint aggregates advisory data per SBOM.
- **Registration pattern**: Follows the existing `Router::new().route("/path", get(handler))` pattern used for all other routes in this module and sibling modules.
- **Module declaration**: Added in alphabetical order among existing module declarations.

### Sibling Parity

Matches the route registration pattern in:
- `sbom/endpoints/mod.rs` (registers `/api/v2/sbom` and `/api/v2/sbom/:id`)
- `package/endpoints/mod.rs` (registers `/api/v2/package`)
- `advisory/endpoints/mod.rs` itself (existing `/api/v2/advisory` routes)

### Note on Route Placement

Alternatively, this route could be registered in `sbom/endpoints/mod.rs` since it is an SBOM-scoped endpoint. However, the task description explicitly places the handler in the advisory module (`modules/fundamental/src/advisory/endpoints/`), and the route registration in `advisory/endpoints/mod.rs`. The task's architecture decision is followed as specified.
