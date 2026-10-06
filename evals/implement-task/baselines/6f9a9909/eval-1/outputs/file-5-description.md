# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory module's endpoint router.

## Current State

The file registers existing advisory routes following the pattern:

```rust
pub mod get;
pub mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
}
```

## Changes

1. Add module declaration for the new endpoint:

```rust
pub mod severity_summary;
```

2. Add the new route to the router function:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
```

### Full Modified Router

```rust
pub mod get;
pub mod list;
pub mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
}
```

## Design Notes

- The route path `/api/v2/sbom/{id}/advisory-summary` lives under the `sbom` URL
  namespace but is registered in the advisory module's router because it is served
  by `AdvisoryService`. This is consistent with the task specification and avoids
  modifying the SBOM module.
- The route uses `:id` (Axum path parameter syntax) matching the existing `:id`
  patterns in sibling routes.

## Conventions Applied

- Route registration follows the existing `Router::new().route(...)` chaining pattern
- Module declaration follows the `pub mod <name>;` pattern in the same file
- Handler reference uses `module::function` pattern (e.g., `severity_summary::get`)
