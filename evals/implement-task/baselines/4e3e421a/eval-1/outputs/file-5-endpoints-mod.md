# File 5 (MODIFY): `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new handler module and route, following the existing
`Router::new().route("/path", get(handler))` chain.

```diff
 mod get;
 mod list;
+mod severity_summary;

 ...

 pub fn router(service: AdvisoryService) -> Router {
     Router::new()
         .route("/api/v2/advisory", get(list::list))
         .route("/api/v2/advisory/{id}", get(get::get))
+        .route(
+            "/api/v2/sbom/{id}/advisory-summary",
+            get(severity_summary::severity_summary),
+        )
         .with_state(service)
 }
```

Notes:
- Function name, state wiring, and any caching layer (`tower-http`) are taken from the existing builder; if the `get` route has a per-route cache layer, apply the same to the new route.
- If siblings are listed in an OpenAPI `#[derive(OpenApi)] paths(...)` block in this file, add `severity_summary::severity_summary` there too.
- The path sits under `/api/v2/sbom/...` but is registered here in the advisory module, as the task's Implementation Notes direct. `server/src/main.rs` already mounts this router, so no change there.
