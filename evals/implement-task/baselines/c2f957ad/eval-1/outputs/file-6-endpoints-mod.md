# File 6 (MODIFY): `modules/fundamental/src/advisory/endpoints/mod.rs`

Declare the new handler module and register its route following the existing
`Router::new().route("/path", get(handler))` chain.

```diff
 mod get;
 mod list;
+mod severity_summary;

 pub fn router(/* existing params, e.g. service: AdvisoryService */) -> Router {
     Router::new()
         .route("/api/v2/advisory", get(list::list))
         .route("/api/v2/advisory/{id}", get(get::get))
+        .route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::get))
         // existing .layer(...caching...) / .with_state(service) remain unchanged and now
         // also apply to the new route
 }
```

If siblings register handlers in an OpenAPI `paths(...)` list (utoipa `OpenApi` derive) in this file,
add `severity_summary::get` there too.

Notes:
- Path-parameter syntax (`{id}` vs `:id`) copied from the existing `/api/v2/advisory/{id}` route.
- Route is placed before the shared caching/state layers so it inherits them (sibling parity).
- `server/src/main.rs` already mounts this router; no change there (as stated in the task).
- The path is under `/api/v2/sbom/...` but owned by the advisory module per the task's Files to Modify;
  verify no conflicting route is registered by the SBOM router (`search_for_pattern "advisory-summary"`).
