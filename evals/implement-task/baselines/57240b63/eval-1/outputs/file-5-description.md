# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose
Register the new severity summary route in the advisory endpoints module.

## Reference Files to Inspect First
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- Read the existing route registrations to understand the `Router::new().route("/path", get(handler))` pattern and how modules are declared.

## Changes

### 1. Add module declaration

Add a `mod severity_summary;` declaration alongside the existing endpoint module declarations (e.g., near `mod get;`):

```rust
mod severity_summary;
```

### 2. Register the new route

Add the new route to the router configuration, following the existing pattern of `Router::new().route(...)`:

```rust
.route(
    "/api/v2/sbom/:id/advisory-summary",
    get(severity_summary::get_advisory_severity_summary),
)
```

## Notes
- The exact path parameter syntax (`:id` vs `{id}`) must be confirmed by reading the existing route registrations in `mod.rs`. Axum uses `:id`, while the task description uses `{id}` -- follow whichever convention the existing code uses.
- The route registration placement should follow alphabetical or logical ordering consistent with existing routes.
- The handler function name (`get_advisory_severity_summary`) must match the function defined in the endpoint handler file (file-2-description.md).
