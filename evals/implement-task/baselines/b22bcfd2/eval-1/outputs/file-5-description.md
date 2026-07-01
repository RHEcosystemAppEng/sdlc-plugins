# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory endpoint module's router.

## Pre-Implementation Inspection

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` to see existing route registration pattern
- `mcp__serena_backend__find_symbol` with `include_body=true` on the route builder function to see exact `Router::new().route(...)` syntax
- Verify import pattern for handler modules (e.g., `mod get;`, `mod list;`)

## Detailed Changes

1. Add module declaration for the new endpoint handler:

```rust
// Existing:
mod get;
mod list;

// Add:
mod severity_summary;
```

2. Add route registration in the router builder function:

```rust
// Existing routes (example):
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    // Add new route:
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Notes

- The route path `/api/v2/sbom/{id}/advisory-summary` is placed in the advisory endpoints module even though it's under the SBOM URL namespace. This is because the functionality is advisory-centric (aggregating advisory severities). Verify this placement during code inspection -- if SBOM endpoints handle their own sub-routes, the route may need to be registered in `modules/fundamental/src/sbom/endpoints/mod.rs` instead.
- The exact path parameter syntax (`:id` vs `{id}`) depends on the Axum version used by the project -- verify against existing route definitions.
- The module declaration (`mod severity_summary;`) placement should be alphabetically ordered with existing declarations.
- The task description says `server/src/main.rs` needs no changes because routes auto-mount via module registration, confirming that adding the route in `endpoints/mod.rs` is sufficient.
