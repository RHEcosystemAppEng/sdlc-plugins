# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose
Register the new severity summary route so that the endpoint is accessible via the API.

## Changes

### Import addition

Add the new endpoint module declaration:

```rust
pub mod severity_summary;
```

This should be added alongside the existing `pub mod get;` and `pub mod list;` declarations.

### Route registration

In the function that builds the advisory endpoints router (likely a `configure` or `routes` function), add:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This should be added to the existing `Router::new()` chain, following the pattern of the existing `.route(...)` registrations for `get.rs` and `list.rs`.

## Conventions Applied
- Follows the `Router::new().route("/path", get(handler))` registration pattern established by existing endpoints.
- Module declaration via `pub mod severity_summary;` matches how `get` and `list` are declared.
- Route path uses `:id` Axum path parameter syntax (matching the existing `/api/v2/advisory/:id` pattern).

## Notes
- The endpoint path is `/api/v2/sbom/{id}/advisory-summary` as specified in the task's API Changes section. The `{id}` placeholder becomes `:id` in Axum route syntax.
- Since `server/main.rs` auto-mounts routes via module registration, no changes are needed in `main.rs`.
