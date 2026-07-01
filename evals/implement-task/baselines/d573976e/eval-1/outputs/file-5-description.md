# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary route in the advisory endpoints module.

## Detailed Changes

### Add module declaration

Add the following line alongside the existing module declarations (near `pub mod get;` and `pub mod list;`):

```rust
pub mod severity_summary;
```

### Add route registration

In the function that builds the router (following the existing `Router::new().route(...)` pattern), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This should be added alongside the existing route registrations for advisory endpoints.

### Import addition

Add the import for the `get` method extractor if not already imported:

```rust
use axum::routing::get;
```

## Conventions Followed

- **Route registration pattern**: follows the existing `Router::new().route("/path", get(handler))` pattern used for all endpoint registrations in this module.
- **Module registration**: uses `pub mod severity_summary;` to register the new endpoint module, matching the pattern of `pub mod get;` and `pub mod list;`.
- **URL path**: uses `:id` parameter syntax consistent with Axum's path parameter extraction.
- **Handler reference**: references the handler via `severity_summary::get_severity_summary`, following the `module::handler` pattern used by other routes.
