# File 5 (MODIFY): `modules/fundamental/src/advisory/endpoints/mod.rs`

1. Declare the handler module alongside `get` and `list`:

```diff
 mod get;
 mod list;
+mod severity_summary;
```

2. Register the route in the existing router builder, following the
   `Router::new().route("/path", get(handler))` pattern:

```diff
     Router::new()
         .route("/api/v2/advisory", get(list::list))
         .route("/api/v2/advisory/{id}", get(get::get))
+        .route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::severity_summary))
```

3. If an OpenAPI `paths(...)` list exists in this module, add `severity_summary::severity_summary`.

Notes:
- Use the same path-parameter syntax as existing routes (`{id}` on Axum 0.8, `:id` on 0.7).
- The path lives under `/api/v2/sbom/...` but is registered in the advisory router, as the
  task specifies. If the advisory router is nested under a `/api/v2/advisory` prefix
  (rather than using absolute paths), the route would resolve to the wrong URL — verify with
  `find_symbol` on the router fn; if nested, raise to the user (registering in the SBOM
  router instead would be out of scope).
- Apply the same caching middleware configuration as sibling GET routes, if any.
- `server/src/main.rs`: no change — the advisory router is already mounted.
