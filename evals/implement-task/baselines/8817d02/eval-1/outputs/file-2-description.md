# File 2: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Change Type
Modify existing file

## Description
Register the new severity summary route in the advisory endpoints module. Add the route for `GET /api/v2/sbom/{id}/advisory-summary` following the existing `Router::new().route()` registration pattern.

## Detailed Changes

### Add module declaration

Add the module declaration for the new endpoint handler:

```rust
pub mod severity_summary;
```

This goes alongside the existing `pub mod get;` and `pub mod list;` declarations.

### Add route registration

In the router construction function (where existing routes are registered), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the pattern of existing `Router::new().route("/path", get(handler))` registrations visible in the sibling endpoint modules.

### Add import

Add the import for the `get` method extractor if not already present:

```rust
use axum::routing::get;
```

## Conventions Followed
- Route registration pattern matches existing endpoints in `mod.rs`
- Module declaration follows alphabetical or logical ordering of existing `pub mod` declarations
- Path parameter uses `:id` syntax consistent with Axum's path extraction
- Route path follows existing API version prefix pattern (`/api/v2/`)
