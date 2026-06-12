# File 6 -- MODIFY: modules/fundamental/src/advisory/endpoints/mod.rs

## Purpose

Register the new severity summary route in the advisory endpoints module so the handler is reachable at `/api/v2/sbom/{id}/advisory-summary`.

## Conventions Applied

- **Route registration pattern:** Follows the existing `Router::new().route("/path", get(handler))` pattern used for other endpoints in this file.
- **Module declaration:** Adds `mod severity_summary;` to declare the new endpoint handler module, consistent with how `get` and `list` modules are declared.

## Detailed Changes

The existing file likely has a structure similar to:

```rust
mod get;
mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
}
```

Add the new module declaration and route:

```rust
mod get;
mod list;
mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::severity_summary),
        )
}
```

## Key Design Decisions

- **Route path:** Uses `/api/v2/sbom/{id}/advisory-summary` as specified in the API Changes section. The route is registered in the advisory module's router even though the path starts with `/sbom/` -- this is because the functionality belongs to the advisory domain (aggregating advisory data), and the SBOM ID is just the lookup key.
- **Module name:** `severity_summary` matches the handler file name, consistent with how `get` and `list` modules are named after their handler files.
- **Route position:** Added after existing routes, maintaining readability.

## Scope

Two changes to this file:
1. Add `mod severity_summary;` module declaration
2. Add `.route(...)` call for the new endpoint
