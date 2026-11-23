# File 5 — MODIFY `modules/fundamental/src/advisory/endpoints/mod.rs`

**Purpose**: register the new handler module and route.

**Inspect first**: `get_symbols_overview` and `find_symbol(<router fn>, include_body=true)` to see the
existing `Router::new().route("/api/v2/advisory", get(list::list_advisories)).route("/api/v2/advisory/:id", get(get::get_advisory))`
chain, the path parameter syntax (`:id` vs `{id}`, which depends on the Axum version), the caching layer, and
any utoipa `OpenApi` derive that lists paths.

**Changes**:

1. Module declaration next to the existing ones:
```rust
mod get;
mod list;
mod severity_summary;   // NEW
```

2. Route added to the existing builder, using the siblings' path param syntax and inheriting the same `tower-http` caching layer and state:
```rust
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    .route(
        "/api/v2/sbom/:id/advisory-summary",
        get(severity_summary::get_severity_summary),
    ) // NEW
    // existing .layer(...) / .with_state(...) unchanged
```

3. If the module has `#[derive(OpenApi)] #[openapi(paths(...), components(schemas(...)))]`, add
`severity_summary::get_severity_summary` to `paths` and `SeveritySummary` to `schemas`.

`server/src/main.rs` already mounts this router, so it is not modified, per the task.
Check for route conflicts: grep the `sbom` endpoints module for `/api/v2/sbom/:id/advisory-summary` (or any route that would shadow it). None is expected.
