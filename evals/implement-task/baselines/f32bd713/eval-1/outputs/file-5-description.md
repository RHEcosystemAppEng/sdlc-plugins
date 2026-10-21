# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: Modify

## Purpose

Register the new `severity_summary` route in the advisory endpoint module's router,
following the existing pattern of `Router::new().route("/path", get(handler))` registrations.

## Pre-implementation inspection

Before modifying this file, would inspect using Serena:

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- see the current route registrations and module declarations
- `mcp__serena_backend__find_symbol` with `include_body=true` on the route registration function/block -- read the exact pattern used to chain `.route()` calls
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/mod.rs` -- cross-reference with sibling module's route registration for consistency
- `mcp__serena_backend__find_referencing_symbols` on the router function -- confirm how server/main.rs mounts it

## Detailed changes

**1. Add module declaration** at the top of the file alongside existing endpoint module declarations:

```rust
pub mod severity_summary;
```

**2. Add route registration** in the router builder, following the existing `.route()` chain pattern.

The new route would be added to the existing `Router::new()` chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

**3. Add import** for the `get` method if not already imported (likely already present from existing routes):

```rust
use axum::routing::get;
```

## Conventions applied

- Module declaration follows existing `pub mod list;` and `pub mod get;` pattern
- Route path uses Axum's `:id` parameter syntax (would verify exact syntax from siblings -- may be `{id}` depending on Axum version)
- Route registration follows the `.route()` chaining pattern from existing registrations
- Handler referenced as `module::function` pattern (`severity_summary::severity_summary`)
- Route placed logically with other advisory-related routes

## Notes

- The exact route path parameter syntax (`:id` vs `{id}`) depends on the Axum version used -- would be confirmed from sibling inspection
- The route path `/api/v2/sbom/:id/advisory-summary` is under the SBOM path namespace but registered in the advisory endpoints module -- this follows the task description and would be verified as consistent with how the server mounts modules
- If the advisory module's routes are mounted under a prefix by the server (e.g., all advisory routes get `/api/v2/advisory` prepended), the route path here would be relative -- would be confirmed from inspection
