# File 5: MODIFY — `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose
Register the new severity_summary route in the advisory endpoints module.

## Changes

Add route registration for the new endpoint:

```rust
pub mod severity_summary;

// In the router function, add:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Conventions Applied

- Follows the existing `Router::new().route("/path", get(handler))` registration pattern
- Module declaration added alongside existing `pub mod list;` and `pub mod get;`
- Route path follows the REST convention of the existing API
