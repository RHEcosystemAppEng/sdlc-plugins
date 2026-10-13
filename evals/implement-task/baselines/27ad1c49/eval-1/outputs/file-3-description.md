# File 3: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary endpoint route so that `GET /api/v2/sbom/{id}/advisory-summary` is accessible.

## Pre-Implementation Inspection

1. `mcp__serena_backend__get_symbols_overview` on this file to see the route registration pattern.
2. `mcp__serena_backend__find_symbol` on the router setup function to see existing `.route()` calls.
3. Check the existing pattern: expected to see `Router::new().route("/path", get(handler))` chaining.

## Changes

### Import the New Handler

Add an import for the severity summary handler module and function:

```rust
mod severity_summary;
```

And the handler function import (depending on how the existing file structures it -- either inline `use` or path-qualified in the route registration).

### Register the Route

Add a new `.route()` call to the existing router chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the existing pattern of `Router::new().route(...)` chaining seen in the sibling `sbom/endpoints/mod.rs` and this file's own route registrations.

### Placement

The new route should be added after existing route registrations, following the convention of the file. Use `mcp__serena_backend__insert_after_symbol` if the routes are in a builder function, or Edit tool if they are in a module-level constant.

## Convention Compliance

- Route path follows RESTful convention and matches the API Changes specification
- Uses `get()` handler registration matching the HTTP method (GET)
- Module declaration follows snake_case naming (`severity_summary`)
- Handler function follows the verb_noun pattern (`get_severity_summary`)
