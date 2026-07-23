# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route by importing the severity_summary handler module and adding it to the router.

## Pre-implementation inspection

Before modifying this file, perform the following inspections:

- **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the current route registration structure. Identify how existing routes are organized (the `Router::new().route(...)` chain) and where the new route should be added.
- **`modules/fundamental/src/sbom/endpoints/mod.rs`** -- Read as a sibling to confirm the route registration pattern is consistent across modules.
- Use `mcp__serena_backend__find_referencing_symbols` on the router function to ensure adding a new route does not conflict with existing route paths.

## Detailed changes

Two changes to the existing file:

### 1. Add module declaration

Add the following line alongside existing module declarations (e.g., after `mod get;` and `mod list;`):

```rust
mod severity_summary;
```

### 2. Register the route

Add the new route to the existing `Router::new()` chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the pattern of existing route registrations like:
```rust
.route("/api/v2/advisory/:id", get(get::get_advisory))
```

## Conventions followed

- Module declaration follows alphabetical or logical ordering with existing declarations
- Route path follows the existing URL pattern (`/api/v2/<entity>/<path>`)
- Handler reference follows the `<module>::<function>` pattern
- Uses Axum's `get()` method handler
