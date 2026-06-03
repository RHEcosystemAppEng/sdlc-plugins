# File 6: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary endpoint route and declare the new endpoint module.

## Detailed Changes

### Add module declaration

Add the following line to the module declarations at the top of the file:

```rust
pub mod severity_summary;
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

- **Module declaration**: Uses `mod severity_summary;` (may be `pub mod` depending on whether sibling modules use `pub`). Follows the existing declaration style of `mod get;` and `mod list;`.
- **Route registration**: Uses `Router::new().route(path, method(handler))` chaining pattern, consistent with existing route registrations.
- **Path parameter syntax**: Uses Axum's `:id` path parameter syntax (or `{id}` depending on the Axum version in use — the task description uses `{id}` in the API spec, but the route registration syntax depends on the Axum version).
- **Handler reference**: References the handler as `severity_summary::severity_summary`, following the `module::function` pattern used by `get::get` and `list::list`.

## Notes

- The route path `/api/v2/sbom/:id/advisory-summary` is nested under the SBOM resource path. While it's registered in the advisory endpoints module (since it uses the `AdvisoryService`), the URL is scoped to an SBOM. This is a deliberate design choice: the functionality logically belongs to the advisory domain (aggregating advisory data), but the resource path reflects the SBOM context.
- If the project uses Axum 0.7+, the path parameter syntax is `/{id}` rather than `/:id`. The implementation should match whichever convention is used in the existing route definitions.
- If the advisory `endpoints/mod.rs` uses a route prefix/nesting pattern, the path may need to be adjusted accordingly (e.g., if all advisory routes are nested under a prefix, the `sbom/:id/advisory-summary` portion would be the relative path).
