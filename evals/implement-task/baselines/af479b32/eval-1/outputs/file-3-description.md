# File 3: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose
Register the new severity summary route in the advisory endpoints module so the endpoint is accessible via the REST API.

## Changes

### Add module declaration
Add a module declaration for the new endpoint file:
```rust
mod severity_summary;
```

### Register the route
In the router builder function/block (where existing routes like `list` and `get` are registered), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the existing pattern of `Router::new().route("/path", get(handler))` chaining visible in the current `mod.rs`.

### Placement
- The `mod severity_summary;` declaration should be placed alongside existing `mod list;` and `mod get;` declarations
- The route registration should be added after existing routes in the router chain

## Impact
- Exposes the new endpoint at `GET /api/v2/sbom/{id}/advisory-summary`
- No changes to existing routes
- The server auto-mounts routes via module registration, so no changes needed in `server/src/main.rs`
