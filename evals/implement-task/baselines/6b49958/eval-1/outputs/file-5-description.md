# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary endpoint route so that it is mounted by the application router.

## Current State (Expected)

The file currently declares the existing endpoint modules and builds a router with their routes:

```rust
mod get;
mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

(Exact path patterns and handler names will be confirmed from the actual file at implementation time.)

## Change

1. Add the new module declaration.
2. Add the new route to the router.

```rust
mod get;
mod list;
mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::get_severity_summary),
        )
}
```

## Detailed Diff

```diff
 mod get;
 mod list;
+mod severity_summary;
 
 pub fn router() -> Router {
     Router::new()
         .route("/api/v2/advisory", get(list::list_advisories))
         .route("/api/v2/advisory/:id", get(get::get_advisory))
+        .route(
+            "/api/v2/sbom/:id/advisory-summary",
+            get(severity_summary::get_severity_summary),
+        )
 }
```

## Design Decisions

- **Route path `/api/v2/sbom/{id}/advisory-summary`:** This is a sub-resource of SBOM, not of advisory. The route is registered in the advisory endpoints module because the business logic lives in `AdvisoryService`, but the URL is SBOM-centric as specified in the task.
- **Module declaration order:** `severity_summary` is added alphabetically after `list`.
- **Path parameter syntax:** Axum uses `:id` syntax; if the project uses `{id}` (utoipa-style in path annotations but `:id` in actual router), the router registration uses `:id`. This will be confirmed from the existing routes at implementation time.

## Alternative Consideration

If the project's convention is to register SBOM sub-resource routes in an SBOM endpoints module rather than the advisory module, the route registration would move to `modules/fundamental/src/sbom/endpoints/mod.rs` instead. However, the task explicitly specifies modifying `advisory/endpoints/mod.rs`, so we follow the task specification. The handler still lives in the advisory endpoints directory since the service method is on `AdvisoryService`.
