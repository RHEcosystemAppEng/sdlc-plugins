# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs`

**Action**: Modify existing file

## Purpose

Register the new severity summary route in the advisory endpoints module. This connects the URL path to the handler function.

## Conventions Applied

- **Route registration pattern**: Follows existing `Router::new().route("/path", get(handler))` pattern used for other endpoints in this file.
- **Module declaration**: Adds `mod severity_summary;` to declare the new endpoint module.
- **Import pattern**: Matches how existing endpoint files are imported and their handlers referenced.

## Detailed Changes

### 1. Add module declaration

Add at the top of the file alongside existing module declarations:

```rust
mod severity_summary;
```

### 2. Add route registration

In the router builder function (where existing routes are registered), add the new route:

```rust
// Before (existing routes, representative):
Router::new()
    .route("/api/v2/advisory", get(list::list))
    .route("/api/v2/advisory/:id", get(get::get))

// After (with new route added):
Router::new()
    .route("/api/v2/advisory", get(list::list))
    .route("/api/v2/advisory/:id", get(get::get))
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

## Design Decisions

- **Route path**: `/api/v2/sbom/:id/advisory-summary` as specified in the task's API Changes section. This nests under the SBOM resource path since the aggregation is per-SBOM, even though the handler lives in the advisory module.
- **HTTP method**: `get` -- this is a read-only aggregation endpoint.
- **Handler reference**: `severity_summary::severity_summary` references the module and function name, following the pattern `get::get` and `list::list` used by existing endpoints.
- **Route placement**: Added after existing advisory routes. The route path is distinct from existing routes so ordering does not affect matching.

## Notes

- The task states `server/src/main.rs` does not need changes because routes auto-mount via module registration. This means the advisory module's router is already mounted in the server configuration, and adding a route here automatically makes it available.
- The route uses `:id` parameter syntax (Axum convention), which maps to the `Path<Id>` extractor in the handler.
