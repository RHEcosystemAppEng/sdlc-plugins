# File 3: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary route and import the handler module so that the endpoint is mounted in the router.

## Current State

The file registers existing advisory routes using the Axum `Router::new().route()` pattern:

```rust
mod list;
mod get;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

## Changes

### 1. Add module declaration

Add the new handler module import alongside existing module declarations:

```rust
mod list;
mod get;
mod severity_summary;
```

### 2. Add route registration

Add the new route to the router chain, following the existing `Router::new().route()` pattern:

```rust
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

## Pattern Compliance

- **Module declaration**: follows `mod list;` / `mod get;` sibling pattern
- **Route registration**: uses `.route("/path", get(handler))` pattern matching existing routes
- **Path format**: uses `:id` parameter syntax consistent with Axum path extractors
- **Handler naming**: follows `<verb>_<resource>` convention (e.g., `get_severity_summary`)

## Note on Route Path

The endpoint path `/api/v2/sbom/{id}/advisory-summary` is nested under the SBOM resource even though the route is registered in the advisory endpoints module. This is because the endpoint conceptually retrieves advisory data scoped to a specific SBOM. The task description explicitly specifies this path.

## Impact

- Adds one new route to the advisory module's router
- No changes to existing routes
- No breaking changes
