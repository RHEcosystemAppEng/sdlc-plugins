# File 2: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory module's endpoint router.

## Detailed Changes

### Add module declaration

Add at the top of the file with the other module declarations:

```rust
mod severity_summary;
```

### Add route registration

Following the existing pattern of `Router::new().route("/path", get(handler))` chaining, add the new route to the router:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This line would be added to the existing `Router::new()` chain alongside the other route registrations in this file.

## Conventions Followed

- Route registration uses Axum's `Router::new().route()` chaining pattern
- Handler function is referenced by module path (`severity_summary::get_severity_summary`)
- Route path follows the REST convention with the SBOM ID as a path parameter
- Uses `get()` method handler for GET endpoint
- Module declared with `mod severity_summary;` alongside existing modules like `get` and `list`
