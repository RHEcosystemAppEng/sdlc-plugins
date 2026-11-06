# File 2 (MODIFY): `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose
Register the new handler module and route, following the existing `Router::new().route("/path", get(handler))` pattern.

## Changes
1. Add the module declaration next to the existing `mod get;` and `mod list;`:
```rust
mod get;
mod list;
mod severity_summary;
```

2. Chain the new route onto the existing router builder:
```rust
Router::new()
    .route("/api/v2/advisory", get(list::list))
    .route("/api/v2/advisory/:id", get(get::get))
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
    // ...existing layers (state / tower-http caching) unchanged
```

## Notes
- Path parameter syntax (`:id` or `{id}`) is copied from the existing routes, depending on the Axum version.
- If this router is `.nest("/api/v2/advisory", ...)`-ed, the new route is added on the outer (un-nested) router so
  the full path is `/api/v2/sbom/{id}/advisory-summary`. This would be flagged to the user, because it's a minor
  cross-resource placement question.
- The caching layer for this route is the same as for the single-resource `get` route.
- `server/src/main.rs` is not changed, because it already mounts this module's router.
