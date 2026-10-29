# File 3: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: Modify (existing file)

## Purpose

Register the new severity summary route in the advisory module's endpoint router so requests to `GET /api/v2/sbom/{id}/advisory-summary` are routed to the new handler.

## Changes

### New import

Add a module declaration and import for the new endpoint:

```rust
mod severity_summary;
```

### Route registration

Add the new route to the existing `Router::new()` chain following the pattern of existing route registrations:

```rust
// Existing routes (for context):
// Router::new()
//     .route("/api/v2/advisory", get(list::list))
//     .route("/api/v2/advisory/:id", get(get::get_by_id))

// Add new route:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Rationale

- Follows the existing `Router::new().route(...)` pattern used by sibling endpoint registrations
- The endpoint path `/api/v2/sbom/{id}/advisory-summary` nests under the SBOM resource since it provides advisory data for a specific SBOM
- Uses `get()` handler mapping consistent with other GET endpoints
- The module declaration `mod severity_summary;` follows the same pattern as other endpoint sub-modules

## Convention Conformance

- Route registration uses `Router::new().route("/path", get(handler))` pattern
- Module declared with `mod` keyword (private, only the router needs access)
- Handler function referenced as `module::function_name`

## Notes

- The task says "register the new route" in this file, and the route pattern places it under the SBOM path namespace. This is consistent with the API design where advisory-summary is a sub-resource of an SBOM.
- `server/src/main.rs` does not need changes since routes auto-mount via module registration (as stated in the task description).
