# File 2: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: Modify (existing file)

## Pre-Implementation Inspection

Before modifying, inspect this file using:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` to see existing route registrations
- Read the file to understand the exact `Router::new().route(...)` pattern and import style

Also inspect the sibling file for pattern reference:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/mod.rs` to confirm the route registration pattern is consistent across modules

## Changes

1. Add a `pub mod severity_summary;` declaration to import the new endpoint module.

2. Add a new route registration for the severity summary endpoint in the module's router function:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the existing `Router::new().route("/path", get(handler))` pattern observed in the sibling route registrations.

### Import addition

```rust
mod severity_summary;
```

### Route registration addition

Add to the existing `Router::new()` chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

The exact syntax (`:id` vs `{id}` for path parameters) will be confirmed by inspecting the existing route registrations in this file.
