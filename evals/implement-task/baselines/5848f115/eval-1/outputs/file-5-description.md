# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory module's endpoint registration.

## Pre-implementation analysis

Before modifying this file:
- Read the file via `mcp__serena_backend__get_symbols_overview` to see the current route registration structure.
- Use Read or `mcp__serena_backend__find_symbol` to see the exact `Router::new().route(...)` chain and understand where to insert the new route.
- Cross-reference with `modules/fundamental/src/sbom/endpoints/mod.rs` via `mcp__serena_backend__get_symbols_overview` to confirm the cross-module registration pattern.

## Detailed changes

Two additions to this file:

### 1. Add module declaration

At the top of the file, alongside existing module declarations (e.g., `mod get;`, `mod list;`), add:

```rust
mod severity_summary;
```

### 2. Register the new route

In the router builder chain, add a new `.route()` call:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))
```

This is inserted into the existing `Router::new()` chain, following the pattern of other route registrations in this file.

## Conventions applied

- Module declaration style matches existing `mod get;`, `mod list;` declarations
- Route registration follows the exact `Router::new().route("/path", get(handler))` pattern used by sibling routes
- Path parameter syntax uses `:id` (Axum convention) matching existing route definitions
- Handler is referenced as `module::handler` matching sibling patterns
