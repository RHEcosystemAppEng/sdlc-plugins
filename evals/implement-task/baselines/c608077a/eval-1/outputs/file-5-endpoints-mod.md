# File 5 — MODIFY `modules/fundamental/src/advisory/endpoints/mod.rs`

Declare the new handler module and register the route following the existing `Router::new().route("/path", get(handler))` pattern.

```diff
 mod get;
 mod list;
+mod severity_summary;

 ...

 pub fn router(service: AdvisoryService) -> Router {
     Router::new()
         .route("/api/v2/advisory", get(list::list))
         .route("/api/v2/advisory/:id", get(get::get))
+        .route(
+            "/api/v2/sbom/:id/advisory-summary",
+            get(severity_summary::severity_summary),
+        )
         .with_state(service)
 }
```

If the module also aggregates OpenAPI paths (e.g. `#[derive(OpenApi)] #[openapi(paths(get::get, list::list))]`), add `severity_summary::severity_summary` and `SeveritySummary` to `paths(...)`/`components(schemas(...))`.

Notes:
- Path parameter syntax (`:id` vs `{id}`) matches the existing routes in the file (depends on Axum version).
- If the advisory router is nested under a `/api/v2/advisory` prefix in `server/src/main.rs` (rather than using absolute paths as above), an SBOM-scoped path cannot be expressed relative to it; in that case stop and flag to the user (options: absolute route on a merged router, or move registration to sbom endpoints — outside listed scope). `server/src/main.rs` is not modified.
