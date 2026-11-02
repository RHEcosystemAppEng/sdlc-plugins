# File 2 — Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`

## What changes

Register the new severity summary route in the advisory endpoints module.

## Code inspection

Before modifying, inspect with `mcp__serena_backend__get_symbols_overview` on `advisory/endpoints/mod.rs` to see the existing route registration pattern (`Router::new().route(...)` calls).

## Detailed changes

1. Add `mod severity_summary;` declaration at the top with the other module imports.

2. In the router function, add the new route following the existing pattern:

```rust
mod severity_summary;

// In the router builder:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
```

## Patterns followed

- Route registration follows `Router::new().route("/path", get(handler))` pattern from existing endpoints
- Module declaration matches sibling modules (`get`, `list`)
