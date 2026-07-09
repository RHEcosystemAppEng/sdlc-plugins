# File 2: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: Modify (existing file)

## Current State

This file contains the route registration for the advisory module's endpoints. It uses `Router::new().route(...)` to register existing routes for list and get handlers (e.g., `/api/v2/advisory` and `/api/v2/advisory/{id}`).

## Changes

### Register new endpoint module

Add module declaration at the top of the file:

```rust
pub mod severity_summary;
```

### Register new route

Add the new route for the severity summary endpoint to the existing Router chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the existing pattern of route registrations in this file, using Axum's `get()` function to bind the handler to the GET method. The route is added to the same `Router::new()` chain alongside existing advisory routes.

**Note**: The endpoint path is `/api/v2/sbom/{id}/advisory-summary` as specified in the API Changes section. The `:id` syntax is Axum's path parameter format.
