# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new advisory summary route in the advisory module's endpoint configuration.

## Detailed Changes

### 1. Add module declaration

Add the following line to the module declarations at the top of the file:

```rust
pub mod severity_summary;
```

### 2. Register the route

Add the new route to the `Router::new()` chain in the route registration function, following the pattern of existing route registrations:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

This should be added alongside the existing routes for `/api/v2/advisory` and `/api/v2/advisory/{id}`.

### 3. Add import

If the `get` function is imported individually (common in Axum projects), ensure it is included in the use statement:

```rust
use axum::routing::get;
```

## Conventions Applied

- **Route registration pattern**: Follows the existing `Router::new().route("/path", get(handler))` pattern used for all endpoint registrations in the module
- **Path convention**: Uses Axum's `:id` path parameter syntax (or `{id}` depending on the Axum version used in the project)
- **Module declaration**: Sub-module registered with `pub mod` at the top of the file, consistent with how `get.rs` and `list.rs` are registered
- **Minimal change**: Only adds the module declaration and one route registration line
- **Route URL**: Uses `/api/v2/sbom/:id/advisory-summary` as specified in the API Changes section of the task
