# File 3: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory endpoints module.

## Pre-Implementation Inspection

Before modifying, would use:
1. `mcp__serena_backend__get_symbols_overview` on this file to see the current route registration structure
2. `mcp__serena_backend__find_symbol` with `include_body=true` on the router function to see the exact `Router::new().route()` call pattern
3. Read the sibling `endpoints/mod.rs` in the `sbom` module (`modules/fundamental/src/sbom/endpoints/mod.rs`) via `mcp__serena_backend__get_symbols_overview` to see if sub-resource routes follow a different pattern

## Changes

### Add module declaration

Add the module declaration for the new endpoint file:

```rust
mod severity_summary;
```

### Register the route

Add the new route to the router. Following the existing pattern of `Router::new().route("/path", get(handler))`:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

The exact placement depends on the existing route registration structure. Would insert after existing advisory routes, or within the SBOM route group if routes are organized by resource.

### Import to add

If not already imported:

```rust
use axum::routing::get;
```

## Notes

- The route path `/api/v2/sbom/{id}/advisory-summary` uses the SBOM resource as the parent, even though the handler lives in the advisory endpoints module. This is because the endpoint aggregates advisory data _for a specific SBOM_.
- The exact Axum path parameter syntax (`:id` vs `{id}` vs `<id>`) depends on the Axum version used by the project -- would verify by inspecting existing route definitions.
- If the project uses a nested router pattern (e.g., advisory routes are nested under an advisory-specific router that is then merged), the route path would be adjusted accordingly.
- Would check whether the SBOM module's `endpoints/mod.rs` already handles routes under `/api/v2/sbom/:id/` and whether this new route should be registered there instead. The task specifies registering in the advisory module, but would verify to avoid route conflicts.
