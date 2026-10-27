# File 4: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose
Register the new severity summary route in the advisory endpoints module.

## Changes

Add import for the new handler and register the route:

```rust
// Add import
mod severity_summary;
use severity_summary::get_severity_summary;

// Add route to existing Router chain
// Before (existing):
//   Router::new()
//       .route("/api/v2/advisory", get(list::list_advisories))
//       .route("/api/v2/advisory/:id", get(get::get_advisory))
//
// After:
//   Router::new()
//       .route("/api/v2/advisory", get(list::list_advisories))
//       .route("/api/v2/advisory/:id", get(get::get_advisory))
//       .route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

## Rationale
- Follows the existing route registration pattern: `Router::new().route("/path", get(handler))`
- Module import pattern matches existing `mod list;` and `mod get;` declarations
- Route path matches the API Changes specification: `GET /api/v2/sbom/{id}/advisory-summary`
