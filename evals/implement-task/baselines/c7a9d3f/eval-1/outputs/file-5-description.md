# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Action: MODIFY

## Purpose

Register the new severity summary route in the advisory endpoints module.

## Detailed Changes

1. Add a `pub mod severity_summary;` declaration to register the new endpoint module.

2. Add the route registration in the router builder, following the existing `Router::new().route(...)` pattern:

```rust
pub mod severity_summary;

// In the router function/builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Key Implementation Details

1. **Module registration**: `pub mod severity_summary;` makes the handler accessible within the endpoints module.

2. **Route path**: `/api/v2/sbom/:id/advisory-summary` -- note that in Axum, path parameters use `:id` syntax (not `{id}` as in the API description, which uses OpenAPI notation). The exact syntax depends on the Axum version used in the project -- newer versions use `/{id}` while older versions use `/:id`. Inspect the existing route registrations in this file to confirm the correct syntax.

3. **HTTP method**: `get(...)` registers this as a GET endpoint, matching the API specification.

4. **Route placement**: insert the new route alongside existing advisory routes, following the ordering pattern used in the file.

## Conventions Applied

- **Route registration**: follows the existing `Router::new().route("/path", get(handler))` pattern observed in sibling endpoint `mod.rs` files.
- **Module declaration**: uses `pub mod` consistent with existing endpoint module declarations (`list`, `get`).
