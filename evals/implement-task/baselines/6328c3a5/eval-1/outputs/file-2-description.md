# File 2: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Pre-implementation Inspection

Before modifying, would use Serena to inspect:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/mod.rs")` -- see the route registration structure
2. `mcp__serena_backend__find_symbol(name_path_pattern="advisory::endpoints", include_body=true)` -- read the full router setup to understand the exact pattern

Also inspect sibling endpoint registrations:
3. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/sbom/endpoints/mod.rs")` -- compare route registration pattern in another module

## Changes

### Add module declaration

Add a `mod severity_summary;` declaration alongside the existing `mod list;` and `mod get;` declarations.

### Register the new route

In the router function (where existing routes like `/api/v2/advisory` are registered), add the new route:

```rust
mod severity_summary;

// In the router setup function, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Placement

The new route registration should be added after the existing advisory route registrations, following the same `Router::new().route(...)` pattern. The exact syntax depends on whether the router uses method chaining or sequential `.route()` calls -- would match the existing pattern found during inspection.

### Convention conformance

- Route path uses kebab-case for URL segments (`advisory-summary`), consistent with REST conventions
- Handler reference follows `module::function` pattern
- Uses `get()` method for GET endpoint, matching Axum conventions
- Registration placed in the advisory endpoints module since this is advisory-domain functionality, even though the URL path starts with `/sbom/` -- this follows the task description's explicit instruction
