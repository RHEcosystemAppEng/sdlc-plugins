# File 2: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Pre-Implementation Inspection

Before modifying this file, read it using `mcp__serena_backend__get_symbols_overview` to see existing route registrations and understand the pattern for how routes are added.

## Changes

### Register the new severity summary route

Add a module declaration and route registration:

```rust
pub mod severity_summary;
```

In the router construction, add:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
```

This follows the existing pattern seen in the registration of `get.rs` and `list.rs` handlers.
