# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new severity summary route in the advisory endpoints router so that `GET /api/v2/sbom/{id}/advisory-summary` is served.

## Detailed Changes

### Current State (expected)

The file contains route registrations using `Router::new().route(...)` pattern, similar to:

```rust
mod list;
mod get;

use axum::{routing::get, Router};

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

### Change

1. Add module declaration for the new endpoint file:
   ```rust
   mod severity_summary;
   ```

2. Add the new route to the router:
   ```rust
   .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
   ```

### Result

```rust
mod list;
mod get;
mod severity_summary;

use axum::{routing::get, Router};

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

### Design Decisions

- **Route path**: `GET /api/v2/sbom/{id}/advisory-summary` as specified in the API Changes section. Note the route uses `:id` Axum path parameter syntax.
- **Route placement**: Added after existing routes in the advisory endpoints module. Although the path is under `/api/v2/sbom/`, it is logically part of the advisory domain since it aggregates advisory data.
- **Handler reference**: Points to `severity_summary::get_severity_summary` in the new endpoint file.

### Conventions Followed

- Route registration follows `Router::new().route("/path", get(handler))` pattern from existing code.
- Module declaration added alongside existing `mod list;` and `mod get;`.
- Uses `get()` from `axum::routing` for GET endpoints.
