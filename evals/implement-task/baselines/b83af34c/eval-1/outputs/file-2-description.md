# File 2: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Pre-implementation Inspection

Before modifying, would use Serena to understand the current state:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/mod.rs")` -- see current route registrations and module declarations.
2. Read the file to see the full route builder pattern.
3. Cross-reference with `modules/fundamental/src/sbom/endpoints/mod.rs` as a sibling to confirm the route registration pattern.

## Changes

### Add module declaration for the new endpoint

Add at the top of the file, alongside existing module declarations:

```rust
mod severity_summary;
```

### Register the new route

In the route builder function (e.g., `pub fn router()` or equivalent), add the new route following the existing pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

**Placement**: After the existing advisory routes, following the same `.route()` chaining pattern.

## Rationale

- Route path `/api/v2/sbom/{id}/advisory-summary` matches the API Changes specification.
- The route is registered under the advisory module's router because the feature aggregates advisory data, even though the path is scoped under `/sbom/{id}`.
- Module declaration `mod severity_summary;` follows the pattern of existing sibling declarations (`mod get;`, `mod list;`).
- Uses `get()` handler binding consistent with the existing REST endpoint registrations in this file.
