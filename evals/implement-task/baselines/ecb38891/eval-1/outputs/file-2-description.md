# File 2: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose
Register the new severity summary route in the advisory module's endpoint registration.

## Pre-Implementation Inspection
Before modifying, read this file to understand how existing routes are registered. Inspect the `Router::new().route(...)` chain to see the pattern for adding new routes.

## Changes

### Add route registration

Add the new route to the existing router chain following the established pattern:

```rust
// Add import for the new handler module
mod severity_summary;

// In the router builder, add:
.route("/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the same `Router::new().route("/path", get(handler))` pattern used for existing routes like `get.rs` and `list.rs` handlers.

## Notes
- The route path `/sbom/:id/advisory-summary` places the endpoint under the SBOM resource since it aggregates advisories for a specific SBOM
- The handler function name `get_severity_summary` follows the `verb_noun` naming convention
