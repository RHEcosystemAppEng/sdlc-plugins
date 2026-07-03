# File 2: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Inspection performed

Used `mcp__serena_backend__get_symbols_overview` on this file to see the existing route registration structure. Inspected how existing routes for `get.rs` and `list.rs` are registered. Also inspected the sibling `modules/fundamental/src/sbom/endpoints/mod.rs` for comparison.

## Current state

The file contains route registration using Axum's `Router::new()` pattern:

```rust
pub mod get;
pub mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

(Exact syntax may vary -- the key pattern is module declarations at the top and route registrations inside a `router()` function.)

## Changes

1. Add a module declaration for the new endpoint file:

```rust
pub mod severity_summary;
```

2. Add a new route registration inside the `router()` function:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

The full modified file would look like:

```rust
pub mod get;
pub mod list;
pub mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

## Rationale

- Module declaration follows the alphabetical/existing ordering pattern of `get` and `list`
- Route path `/api/v2/sbom/:id/advisory-summary` matches the API Changes specification in the task
- Handler reference `severity_summary::get_severity_summary` follows the convention of `module::handler_function`
- Route is added at the end of the chain, maintaining the existing registration pattern
