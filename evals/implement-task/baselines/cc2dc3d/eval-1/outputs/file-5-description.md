# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: Modify existing file

## Purpose

Register the new severity summary endpoint route and declare the new endpoint sub-module. This integrates the new handler into the existing advisory endpoint router.

## Detailed Changes

### Add module declaration

Add at the top of the file alongside existing module declarations:

```rust
mod severity_summary;
```

### Add route registration

In the router builder function (where existing routes like `/api/v2/advisory` and `/api/v2/advisory/{id}` are registered), add the new route:

```rust
.route(
    "/api/v2/sbom/:id/advisory-summary",
    get(severity_summary::get_severity_summary),
)
```

This would be added to the existing `Router::new()` chain, following the pattern of the existing `.route("/path", get(handler))` registrations.

## Conventions Applied

- **Route registration**: follows the existing `Router::new().route("/path", get(handler))` pattern visible in `endpoints/mod.rs`
- **Module declaration**: `mod severity_summary;` follows the pattern of existing declarations for `get` and `list` sub-modules
- **Path convention**: uses `:id` parameter syntax consistent with existing Axum route definitions
- **Handler reference**: references the handler as `severity_summary::get_severity_summary`, following the `<module>::<function>` pattern

## Notes

- The exact position in the route chain and any additional middleware (e.g., caching via tower-http) would be confirmed by reading the current `mod.rs` content via Serena
- The route path uses `/api/v2/sbom/:id/advisory-summary` as specified in the API Changes section of the task
