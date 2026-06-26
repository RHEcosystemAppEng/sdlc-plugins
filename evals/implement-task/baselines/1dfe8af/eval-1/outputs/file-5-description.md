# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose
Register the new severity summary route in the advisory endpoints module.

## Pre-implementation inspection
- Read `modules/fundamental/src/advisory/endpoints/mod.rs` to see existing route registrations and understand the exact pattern.
- Expected to find something like:
  ```rust
  pub mod get;
  pub mod list;

  pub fn router() -> Router {
      Router::new()
          .route("/api/v2/advisory", get(list::list_advisories))
          .route("/api/v2/advisory/:id", get(get::get_advisory))
  }
  ```
- Also read `modules/fundamental/src/sbom/endpoints/mod.rs` (cross-module sibling) to confirm route registration pattern is consistent.

## Detailed Changes

### Add module declaration

Add the module declaration for the new handler file:

```rust
pub mod severity_summary;
```

### Add route registration

Add the new route to the router function:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Placement
- Module declaration added alongside existing `pub mod get;` and `pub mod list;`.
- Route added to the existing `Router::new()` chain, following the pattern of existing `.route()` calls.

### Conventions followed
- Route path follows REST conventions and matches the API Changes section: `/api/v2/sbom/{id}/advisory-summary`.
- Note: Axum uses `:id` syntax for path params (not `{id}`), so the actual route string would be `/api/v2/sbom/:id/advisory-summary`. The exact syntax (`:id` vs `{id}`) would be confirmed from sibling route definitions.
- Handler reference follows `module::function` pattern matching siblings.
- Uses `get()` method wrapper for GET endpoints, matching existing registrations.

### Notes
- The route is mounted under `/api/v2/sbom/{id}/...` even though it lives in the advisory endpoints module. This is because the endpoint is SBOM-scoped (returns advisory data for a specific SBOM). The exact mounting strategy would be confirmed from sibling analysis -- it may need to be registered in the sbom endpoints module instead, depending on how the server mounts routes. The task description says to register it in advisory endpoints, so we follow that unless sibling analysis shows otherwise.
