# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Action: MODIFY

## Purpose
Register the new severity summary endpoint route and import the handler module.

## Conventions Applied
- Route registration via `Router::new().route("/path", get(handler))` (sibling pattern from existing route registrations)
- Module declaration via `pub mod severity_summary;` alongside existing `pub mod get;` and `pub mod list;`
- Import the handler function for use in route registration

## Detailed Changes

### 1. Add module declaration

Add the following line alongside existing module declarations:

```rust
pub mod severity_summary;
```

### 2. Add import for the handler

Add the import for the new handler function:

```rust
use severity_summary::get_severity_summary;
```

### 3. Register the route

Add the new route to the existing `Router` builder chain. Insert the following `.route()` call:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

The full registration in context would look like (assuming existing routes are already present):

```rust
pub mod get;
pub mod list;
pub mod severity_summary;

use axum::{routing::get, Router};
use get::get_advisory;
use list::list_advisories;
use severity_summary::get_severity_summary;

pub fn router() -> Router<...> {
    Router::new()
        .route("/api/v2/advisory", get(list_advisories))
        .route("/api/v2/advisory/:id", get(get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
}
```

## Rationale
- The route path `/api/v2/sbom/{id}/advisory-summary` is registered using Axum's `:id` path parameter syntax
- The route is added to the advisory module's router because the endpoint serves advisory data (severity counts), even though the path starts with `/sbom/` -- this is an advisory-centric view of SBOM-linked data
- Following the existing pattern where each module's `endpoints/mod.rs` registers all routes for that domain
- The route registration is minimal and follows the exact `Router::new().route()` pattern used by sibling routes
