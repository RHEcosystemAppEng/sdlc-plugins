# File 6: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary endpoint route and declare the new endpoint module so the handler is wired into the application's router.

## Detailed Changes

### Add module declaration

Add the following line to the module declarations at the top of the file:

```rust
mod severity_summary;
```

### Add route registration

Add the new route to the existing `Router::new()` chain in the route registration function. Following the existing pattern of `Router::new().route("/path", get(handler))` registrations:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### Before (expected current state)

```rust
mod get;
mod list;

// ... in the route registration function:
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
}
```

### After

```rust
mod get;
mod list;
mod severity_summary;

// ... in the route registration function:
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
}
```

## Conventions Followed

- **Module declaration**: Uses `mod severity_summary;` following the existing declaration style of `mod get;` and `mod list;` in this file. Uses `mod` (not `pub mod`) if sibling declarations are private; uses `pub mod` if they are public.
- **Route registration**: Uses `Router::new().route(path, method(handler))` chaining pattern, consistent with existing route registrations.
- **Path parameter syntax**: Uses `:id` or `{id}` depending on the Axum version in use. The task description uses `{id}` in the API spec, but the route registration syntax must match the Axum version. Would verify by checking the existing route definitions.
- **Handler reference**: References the handler as `severity_summary::severity_summary`, following the `module::function` pattern used by `get::get` and `list::list`.

## Notes

- The route path `/api/v2/sbom/:id/advisory-summary` is nested under the SBOM resource path, even though it is registered in the advisory endpoints module. This is because the functionality logically belongs to the advisory domain (aggregating advisory data), but the URL reflects the SBOM context (querying advisories for a specific SBOM). This cross-domain routing is a deliberate design choice from the task description.
- If the project uses Axum 0.7+, the path parameter syntax is `/{id}` rather than `/:id`. The implementation should match whichever convention is used in the existing route definitions.
- If the advisory `endpoints/mod.rs` uses a route prefix or nesting pattern (e.g., all routes share a common prefix), the path may need adjustment. The exact pattern would be determined by inspecting the existing file structure.
