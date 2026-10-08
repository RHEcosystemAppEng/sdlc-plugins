# File 2: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new `/api/v2/sbom/{id}/advisory-summary` route in the advisory endpoints module.

## Pre-Implementation Analysis

Before modifying, would use Serena to inspect:
- `mcp__serena_backend__get_symbols_overview` on this file to understand the route registration structure
- `mcp__serena_backend__find_symbol` on the router setup function to see existing `.route()` calls
- Sibling analysis: `modules/fundamental/src/sbom/endpoints/mod.rs` for cross-module route registration comparison

## Changes

### Add module declaration for the new endpoint file

At the top of the file alongside existing module declarations:

```rust
mod severity_summary;
```

### Register the new route

In the router builder function, add a new `.route()` call following the existing pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the existing pattern of `Router::new().route("/path", get(handler))` registrations seen in sibling endpoint `mod.rs` files.

### Add import

If not already covered by the module declaration pattern, add the import for the handler function from the new endpoint module.

## Key Decisions

- **Route path**: `/api/v2/sbom/:id/advisory-summary` -- follows Axum path parameter syntax (`:id` for path params) and the RESTful pattern of the existing API
- **HTTP method**: `get()` -- read-only aggregation endpoint
- **Handler reference**: `severity_summary::get_severity_summary` -- follows the `module::handler` naming convention
- **Placement**: Added after existing route registrations to maintain alphabetical/logical ordering
