# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory endpoint module's router, making the `GET /api/v2/sbom/{id}/advisory-summary` endpoint accessible.

## Sibling files inspected

- `modules/fundamental/src/advisory/endpoints/mod.rs` (current state) -- Contains `mod get;` and `mod list;` declarations, plus a router function that composes routes using `Router::new().route(...)`.
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Cross-module sibling showing the same route registration pattern.

## Conventions applied

- Module declaration: `mod severity_summary;` (private mod, only the route function is exposed)
- Route registration: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))` added to the existing Router chain
- Axum `get()` function wrapper for GET handlers

## Detailed changes

### Add module declaration

```rust
// Existing:
mod get;
mod list;

// Add:
mod severity_summary;
```

### Add route registration

In the router function (the function that builds and returns the `Router`), add the new route:

```rust
// Existing pattern (approximate):
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    // Add:
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

Note: The exact route path parameter syntax (`:id` vs `{id}`) would be confirmed by inspecting the actual `get.rs` handler and existing route registrations via Serena. Axum uses `:id` syntax for path parameters.

## Rationale

- The new route is registered alongside existing advisory routes, keeping all advisory-related endpoint routing in one place.
- The path `/api/v2/sbom/:id/advisory-summary` nests under the SBOM resource since the summary is scoped to a specific SBOM, matching the API Changes specification.
- Using `get()` wrapper is consistent with all other GET endpoint registrations in the codebase.
- The `mod severity_summary;` declaration is private (not `pub mod`) because only the route registration needs to reference the handler -- external callers access it via the HTTP route, not Rust imports.
