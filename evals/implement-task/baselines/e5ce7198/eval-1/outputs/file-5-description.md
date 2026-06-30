# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new severity summary endpoint route in the advisory module's endpoint router, and declare the new endpoint sub-module.

## Pre-Modification Inspection

Before making changes, inspect via Serena:
1. `mcp__serena_backend__get_symbols_overview` on the file to see current route registrations
2. Read the file to understand the exact syntax for module declarations and route registration
3. Check how `get.rs` and `list.rs` are registered as sub-modules and routes

## Detailed Changes

### Add module declaration

Add `pub mod severity_summary;` alongside the existing module declarations:

```rust
pub mod get;
pub mod list;
pub mod severity_summary;  // NEW
```

### Add route registration

In the router function/builder, add the new route following the existing pattern:

```rust
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))
```

The exact syntax depends on how routes are currently registered -- the route is added to the existing `Router::new()` chain using `.route()`.

### Design Decisions

- **Route path**: `/api/v2/sbom/:id/advisory-summary` -- uses Axum's `:id` path parameter syntax
- **HTTP method**: `get()` handler registration, matching the GET method specified in the API Changes section
- **Module declaration**: `pub mod severity_summary;` follows the same pattern as existing `pub mod get;` and `pub mod list;`
- **No changes to server/main.rs**: the task description confirms routes auto-mount via module registration, so only the module-level `mod.rs` needs updating

### Convention Compliance

- Route registration follows the exact pattern of existing routes in the same file
- Module declaration order: alphabetical or following existing ordering convention (determined by inspecting the file)
- Uses Axum's `get()` function for route handler binding
