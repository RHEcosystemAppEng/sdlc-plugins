# File 2: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

**Action:** Modify (register new route)

## Pre-implementation inspection

Before modifying this file, inspect it using `mcp__serena_backend__get_symbols_overview` to understand the existing route registration pattern. Also read the sibling file `modules/fundamental/src/advisory/endpoints/get.rs` to see a concrete handler example, and `modules/fundamental/src/sbom/endpoints/mod.rs` to confirm the route registration pattern is consistent across modules.

## Changes

1. Add a module declaration for the new endpoint handler:

```rust
pub mod severity_summary;
```

2. Register the new route in the router builder, following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

**Pattern conformance:**
- Follows the existing registration pattern: `Router::new().route("/path", get(handler))`
- Route path follows the REST convention for sub-resources: `/api/v2/sbom/{id}/advisory-summary`
- Handler function reference uses the `module::function` pattern consistent with how `get.rs` and `list.rs` handlers are referenced
