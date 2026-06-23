# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory module's endpoint configuration.

## Sibling Reference

Follows the existing route registration pattern in this file, which uses `Router::new().route("/path", get(handler))` pattern. Also references the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for SBOM-scoped routes.

## Detailed Changes

### Add module declaration

At the top of the file, alongside existing module declarations:

```rust
// Existing:
mod list;
mod get;

// Add:
mod severity_summary;
```

### Add route registration

In the router builder function, add the new route alongside existing routes:

```rust
// Existing routes (example pattern):
// Router::new()
//     .route("/api/v2/advisory", get(list::list_advisories))
//     .route("/api/v2/advisory/:id", get(get::get_advisory))

// Add:
//     .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Key Design Decisions

- **Route path**: Uses `/api/v2/sbom/{id}/advisory-summary` as specified in the task's API Changes section. The endpoint is scoped under SBOM because it aggregates advisories for a specific SBOM.
- **Module registration**: The `mod severity_summary;` declaration follows the alphabetical or logical ordering of existing module declarations in the file.
- **Handler reference**: Uses `severity_summary::get_severity_summary` following the `<module>::<handler_function>` naming convention visible in sibling route registrations.
- **HTTP method**: Uses `get()` since this is a read-only aggregation endpoint (no side effects).

## Note on Route Placement

The route is registered in the advisory endpoints module because the underlying service logic is in `AdvisoryService`. However, the URL path is under `/api/v2/sbom/{id}/...` since it's an SBOM-scoped view. The actual placement depends on how the existing codebase organizes cross-entity routes. If the SBOM endpoints module owns all `/api/v2/sbom/...` routes, the route registration might belong in `modules/fundamental/src/sbom/endpoints/mod.rs` instead. This would be determined by inspecting the actual file during implementation.
