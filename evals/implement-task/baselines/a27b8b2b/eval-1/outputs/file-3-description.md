# File 3: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary endpoint route so it is reachable via the HTTP router.

## Pre-implementation inspection

Before modifying, inspect this file using:
1. `mcp__serena_backend__get_symbols_overview` to see the current route registration structure.
2. `mcp__serena_backend__find_symbol` on the router configuration function to read the existing `Router::new().route()` chain and understand the pattern for adding new routes.

Also inspect `modules/fundamental/src/advisory/endpoints/get.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` to confirm how handler functions are imported and referenced in route registration.

## Changes

1. Add a module declaration for the new endpoint file:

```rust
// Existing module declarations:
mod get;
mod list;

// Add:
mod severity_summary;
```

2. Add the route registration in the router builder function. Follow the existing pattern of `Router::new().route("/path", get(handler))`:

```rust
// In the router configuration function, add the new route:
.route(
    "/api/v2/sbom/:id/advisory-summary",
    get(severity_summary::severity_summary)
)
```

The exact placement follows the existing route ordering pattern (alphabetical or grouped by resource). The route is scoped under `/api/v2/sbom/{id}/` because it returns advisory data for a specific SBOM, matching the API design in the task description.

## Rationale

The route path `/api/v2/sbom/{id}/advisory-summary` is under the SBOM resource namespace because the endpoint returns advisory data scoped to a specific SBOM. Registering it in the advisory endpoints module keeps the handler code co-located with other advisory-related handlers, while the route path correctly reflects the SBOM-scoped nature of the data.

## Conventions applied

- **Module declaration:** `mod severity_summary;` following the pattern of `mod get;` and `mod list;`
- **Route registration:** `Router::new().route("/path", get(handler))` pattern
- **Path parameter syntax:** Axum uses `:id` for path parameters in route definitions
