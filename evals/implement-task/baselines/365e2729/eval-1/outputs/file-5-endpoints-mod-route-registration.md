# File 5 (MODIFY): `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose
Declare the new handler module and register the route.

## Changes

1. Add the module declaration next to the existing ones:

```rust
mod get;
mod list;
mod severity_summary;   // NEW
```

2. Add the route to the existing router builder, following the
   `Router::new().route("/path", get(handler))` pattern:

```rust
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/{id}", get(get::get))
        // NEW: advisory severity aggregation for an SBOM
        .route(
            "/api/v2/sbom/{id}/advisory-summary",
            get(severity_summary::get_severity_summary),
        )
    // ... existing layers (tower-http cache config) unchanged ...
}
```

3. If the module has an OpenAPI aggregation (`#[derive(OpenApi)] #[openapi(paths(...))]`), add
   `severity_summary::get_severity_summary` to `paths(...)` and `SeveritySummary` to
   `components(schemas(...))`.

## Notes
- If the advisory router is mounted under a nested `/api/v2/advisory` prefix rather than with full
  paths, registering `/api/v2/sbom/{id}/advisory-summary` here would produce the wrong path. In
  that case the route has to be added at the level where full paths are registered. This would be
  confirmed by reading `mod.rs` and how `server/src/main.rs` mounts it, and raised with the user
  if it means touching an unlisted file (see conventions.md, conflict 1).
- The route path segment style (`{id}` vs `:id`) copies whatever the existing registrations use.
- If sibling routes attach a per-route caching layer, apply the same one here.
- `server/src/main.rs` needs no change because the advisory router is already mounted.
