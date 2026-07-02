# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary endpoint route in the advisory module's route configuration.

## Detailed Changes

### Inspection before modification

Use `mcp__serena_backend__get_symbols_overview` on this file to see the existing route registration pattern. Inspect how `get.rs` and `list.rs` handlers are imported and registered.

### Changes

1. **Add module declaration** at the top of the file:
   ```rust
   mod severity_summary;
   ```

2. **Register the route** in the Router builder, following the existing pattern:
   ```rust
   .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
   ```

   This would be added alongside the existing route registrations like:
   ```rust
   .route("/api/v2/advisory", get(list::list))
   .route("/api/v2/advisory/:id", get(get::get))
   ```

### Placement

The route registration would be placed in the same Router chain where other routes are defined. The exact insertion point depends on the file's current structure, which would be confirmed during Step 4 inspection.

## Conventions followed

- Module declaration follows the same `mod <name>;` pattern as sibling modules (`mod get;`, `mod list;`)
- Route registration follows the `Router::new().route("/path", get(handler))` pattern documented in the Implementation Notes
- Path parameter uses `:id` syntax consistent with Axum's path extractor
