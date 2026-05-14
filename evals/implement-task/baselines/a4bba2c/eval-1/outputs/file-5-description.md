# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary endpoint route so that `GET /api/v2/sbom/{id}/advisory-summary` is served by the new handler. This requires declaring the new endpoint module and adding the route to the existing router.

## Sibling Reference

- Current contents of `modules/fundamental/src/advisory/endpoints/mod.rs` — existing route registrations for `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}`
- `modules/fundamental/src/sbom/endpoints/mod.rs` — sibling module route registration for cross-reference

## Changes

### 1. Add module declaration

Add the following line alongside the existing `mod get;` and `mod list;` declarations:

```rust
mod severity_summary;
```

### 2. Add route registration

Inside the router builder function (where existing `.route(...)` calls are chained), add:

```rust
.route(
    "/api/v2/sbom/{id}/advisory-summary",
    get(severity_summary::get_severity_summary),
)
```

This should be appended after the existing route registrations.

## Example of modified file structure

```rust
mod get;
mod list;
mod severity_summary;

use axum::{routing::get, Router};

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/{id}", get(get::get_advisory))
        .route(
            "/api/v2/sbom/{id}/advisory-summary",
            get(severity_summary::get_severity_summary),
        )
}
```

## Conventions Followed

- Module declaration follows existing `mod` declarations — consistent ordering
- Route string follows RESTful convention: resource scoped under SBOM with advisory context
- Handler reference uses `module::function` pattern — matches existing route registrations
- Route registered within the advisory module's router even though the path is under `/sbom/` — appropriate because the advisory module owns the aggregation logic
- Uses `get()` from `axum::routing` which is already imported in this file

## Notes

- The exact router builder function name and `AppState` type should be confirmed by reading the actual `mod.rs` file during pre-implementation analysis
- If the project uses Axum's nested routing (`Router::nest`), the path prefix may differ; the full path shown assumes flat route registration
- Path parameter syntax (`{id}` vs `:id`) depends on the Axum version; Axum 0.7+ uses `/{id}` syntax, older versions use `/:id`
