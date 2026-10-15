# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

## Operation: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route and declare the `severity_summary` endpoint module, so that Axum can route incoming requests to the handler.

## Sibling Reference

This file already registers routes for `GET /api/v2/advisory` (list) and `GET /api/v2/advisory/{id}` (get). The route registration follows the `Router::new().route("/path", get(handler))` pattern.

## Detailed Changes

### 1. Add module declaration

Add the module declaration for the new endpoint file:

```rust
mod severity_summary;
```

### 2. Add use statement

Import the handler function:

```rust
use severity_summary::get_advisory_severity_summary;
```

### 3. Register the route

Add the new route to the router builder. The exact insertion point depends on the existing router construction (would be confirmed via `get_symbols_overview` on this file):

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(get_advisory_severity_summary))
```

### Before (approximate structure)

```rust
mod get;
mod list;

use get::get_advisory;
use list::list_advisories;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list_advisories))
        .route("/api/v2/advisory/:id", get(get_advisory))
}
```

### After

```rust
mod get;
mod list;
mod severity_summary;

use get::get_advisory;
use list::list_advisories;
use severity_summary::get_advisory_severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list_advisories))
        .route("/api/v2/advisory/:id", get(get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(get_advisory_severity_summary))
}
```

## Design Decisions

- **Route path**: `/api/v2/sbom/:id/advisory-summary` places the endpoint under the SBOM resource, matching the API Changes specification. The endpoint logically belongs to the SBOM context since it aggregates advisory data for a specific SBOM.
- **Registration in advisory module**: Even though the route is under `/api/v2/sbom/`, the advisory module owns the business logic. The route is registered here because the handler and service live in the advisory module. This follows the implementation notes which specify registration in `modules/fundamental/src/advisory/endpoints/mod.rs`.
- **Path parameter syntax**: Uses `:id` (Axum's path parameter syntax). Would confirm the exact syntax (`:id` vs `{id}`) by inspecting sibling routes.

## Note on Route Path Convention

The route `/api/v2/sbom/:id/advisory-summary` is nested under the SBOM path but registered in the advisory endpoints module. This cross-cutting route pattern would be verified against existing routes in `modules/fundamental/src/sbom/endpoints/mod.rs` to ensure no path conflicts. If the project convention requires SBOM-scoped routes to be registered in the SBOM module instead, this would be flagged during the contract and sibling parity check in Step 9.

## Conventions Applied

- `mod <name>;` for module declaration
- `use <module>::<handler>;` for import
- `.route("/path", get(handler))` chained builder pattern
- Routes use the `/api/v2/` prefix consistently
