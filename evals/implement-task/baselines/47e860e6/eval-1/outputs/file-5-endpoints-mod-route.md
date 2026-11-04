# File 5 — MODIFY `modules/fundamental/src/advisory/endpoints/mod.rs`

Declare the new handler module and register the route following the existing `Router::new().route("/path", get(handler))` chain.

```diff
 mod get;
 mod list;
+mod severity_summary;

 pub fn router(service: AdvisoryService) -> Router {
     Router::new()
         .route("/api/v2/advisory", get(list::list))
         .route("/api/v2/advisory/:id", get(get::get))
+        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
         // existing tower-http caching layer / .with_state(service) unchanged
         .with_state(service)
 }
```

Notes:
- Path-parameter syntax (`:id` vs `{id}`) copied from sibling routes (depends on Axum version).
- If the module uses a utoipa `OpenApi` derive listing paths, add `severity_summary::get` to its `paths(...)` list.
- If the advisory router is nested under `/api/v2/advisory` (via `Router::nest`), the absolute path above would be wrong — flagged to the user before implementing (see plan.md).
- `server/src/main.rs` is not modified: it already mounts the advisory router.
