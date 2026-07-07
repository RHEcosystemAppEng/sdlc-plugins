# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose
Register the new severity summary endpoint module and route.

## Changes

### 1. Add module declaration

At the top of the file, add alongside existing endpoint module declarations:

```rust
mod severity_summary;
```

### 2. Register the route

In the function that builds the router (typically `pub fn routes() -> Router<AppState>` or similar), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This should be added within the existing `Router::new()` chain, grouped logically with other advisory-related routes.

## Example Context

If the existing code looks like:

```rust
mod get;
mod list;

use axum::{routing::get as axum_get, Router};
use crate::AppState;

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory/:id", axum_get(get::get_advisory))
        .route("/api/v2/advisory", axum_get(list::list_advisories))
}
```

It becomes:

```rust
mod get;
mod list;
mod severity_summary;

use axum::{routing::get as axum_get, Router};
use crate::AppState;

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory/:id", axum_get(get::get_advisory))
        .route("/api/v2/advisory", axum_get(list::list_advisories))
        .route("/api/v2/sbom/:id/advisory-summary", axum_get(severity_summary::get_severity_summary))
}
```

## Notes

- The exact route registration syntax (`:id` vs `{id}`) depends on the Axum version used by the project. Axum v0.6 uses `:id`, Axum v0.7+ uses `{id}`. Will be determined by inspecting existing routes during implementation.
- The route path `/api/v2/sbom/{id}/advisory-summary` is under the SBOM namespace even though the handler lives in the advisory module. This is intentional per the task description — the endpoint conceptually answers "what advisories affect this SBOM."
