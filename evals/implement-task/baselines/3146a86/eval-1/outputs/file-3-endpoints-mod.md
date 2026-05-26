# File 3 — Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`

## Current State (inferred from symbol inspection)

```rust
use super::endpoints::{list, get};
use axum::Router;
use axum::routing::get as get_method;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get_method(list::list_advisories))
        .route("/api/v2/advisory/{id}", get_method(get::get_advisory))
}
```

## Change Required

1. Add `pub mod severity_summary;` to declare the new handler module.
2. Import `severity_summary::get_advisory_summary` handler.
3. Add `.route("/api/v2/sbom/{id}/advisory-summary", get_method(severity_summary::get_advisory_summary))` to the router chain.

## After Change

```rust
pub mod get;
pub mod list;
pub mod severity_summary;

use axum::Router;
use axum::routing::get as get_method;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get_method(list::list_advisories))
        .route("/api/v2/advisory/{id}", get_method(get::get_advisory))
        .route(
            "/api/v2/sbom/{id}/advisory-summary",
            get_method(severity_summary::get_advisory_summary),
        )
}
```

## Notes

- The new route path (`/api/v2/sbom/{id}/advisory-summary`) is under the `sbom` resource, but registered in the advisory module's router because the feature aggregates advisory data for an SBOM. This matches the task description's implementation notes.
- `{id}` follows Axum's path parameter syntax (curly braces, no colon), consistent with existing `{id}` in `/api/v2/advisory/{id}`.
- Module declaration `pub mod severity_summary;` is added in alphabetical order.

## Inspection Steps

1. `mcp__serena_backend__find_symbol` with `include_body=true` on the `router` function in `endpoints/mod.rs` — read the exact current route registrations.
2. Confirm the `get` import alias used (some files alias `axum::routing::get` to avoid shadowing).
3. Use `mcp__serena_backend__replace_symbol_body` on the `router` function to add the new route, or Edit tool as fallback.
