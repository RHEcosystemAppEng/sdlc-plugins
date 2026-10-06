# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` endpoint handler module and add the route
for `GET /api/v2/sbom/{id}/advisory-summary` to the advisory module's router.

## Pre-implementation inspection

Before modifying, inspect the file:
```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/mod.rs")
```

Read the full file to understand:
- How sub-modules are declared (`mod get;`, `mod list;`)
- How routes are registered (`Router::new().route(...)`)
- Whether routes are grouped in a single function or built incrementally

## Changes

### 1. Add module declaration

Add to the module declarations section:
```rust
mod severity_summary;
```

Place it after existing `mod` declarations, following alphabetical or logical order.

### 2. Register the route

Add to the router builder (following the existing `.route()` pattern):
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

The exact Axum path parameter syntax (`:id` vs `{id}`) will be determined by
reading the existing route registrations in this file. The task description uses
`{id}` in the API path, but Axum uses `:id` -- follow whatever syntax the existing
routes use.

## Design decisions

- **Route path**: `/api/v2/sbom/:id/advisory-summary` -- this is under the sbom namespace since the query is "for a given SBOM," even though the endpoint aggregates advisory data. This matches the task specification.
- **HTTP method**: `get()` -- read-only aggregation endpoint
- **No middleware changes**: No additional caching or authentication middleware beyond what the router already applies to all routes

## Convention conformance

- Module declaration style matches siblings (`mod get;`, `mod list;`)
- Route registration follows `Router::new().route("/path", get(handler))` pattern
- Handler reference uses `module::function` syntax (e.g., `severity_summary::get_advisory_summary`)
