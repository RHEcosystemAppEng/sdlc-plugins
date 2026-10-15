# File 6: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Purpose

Register the new severity summary endpoint route so it is accessible via the HTTP server.

## Detailed Changes

### Add module import

Add at the top of the file alongside existing endpoint module declarations:

```rust
mod severity_summary;
```

### Add route registration

In the route registration function (where `Router::new().route(...)` calls are chained),
add:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### Before (expected current state)

```rust
mod list;
mod get;

pub fn router() -> Router {
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

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
}
```

### Design Decisions

- **Route path**: `/api/v2/sbom/:id/advisory-summary` matches the API spec in the task
  description. The path is under `/sbom` (not `/advisory`) because the resource is
  scoped to a specific SBOM.
- **Registration pattern**: follows the exact `Router::new().route()` chaining pattern
  established in the existing `endpoints/mod.rs`.
- **Module declaration**: adds `mod severity_summary;` to make the handler module
  accessible, following the pattern of `mod list;` and `mod get;`.

### Convention Conformance

- Route registration follows the `Router::new().route("/path", get(handler))` pattern
  from sibling endpoint registrations.
- Module declared alongside existing handler modules.
- Path parameter uses Axum's `:id` syntax (or `{id}` depending on which version of
  Axum the project uses - would verify by reading sibling routes).

### Note on Route Placement

The route is registered in the advisory module's `endpoints/mod.rs` because the handler
lives in the advisory module and uses the advisory service. Even though the URL path
starts with `/sbom/`, the advisory module is the correct home because the endpoint
aggregates advisory data. The `server/src/main.rs` mounts all module routers
automatically, so no changes are needed there (confirmed by the task description).
