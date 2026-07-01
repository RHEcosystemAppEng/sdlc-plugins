# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory endpoint module's route configuration.

## Detailed Changes

### Add module declaration

Add at the top of the file alongside existing module declarations:

```rust
pub mod severity_summary;
```

### Add route registration

In the route registration function (likely a function that returns a `Router`), add the new route following the existing pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Before (expected current state)

```rust
pub mod get;
pub mod list;

// ... route registration function
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

### After

```rust
pub mod get;
pub mod list;
pub mod severity_summary;

// ... route registration function
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

## Conventions Applied

- **Module declaration**: `pub mod severity_summary;` added alphabetically with sibling module declarations
- **Route registration**: follows the existing `Router::new().route("/path", get(handler))` pattern documented in Implementation Notes
- **Route path**: uses the path specified in the API Changes section: `/api/v2/sbom/{id}/advisory-summary`
- **Handler reference**: uses the `module::function` pattern matching siblings

## Design Note

The route `/api/v2/sbom/{id}/advisory-summary` is registered in the advisory endpoints module despite being scoped under the SBOM URL path. This is because the business logic belongs to the advisory domain (it aggregates advisory data). The route is mounted here because the advisory service owns the aggregation logic. This cross-referencing is common in domain-driven architectures where the URL structure reflects the consumer's perspective (SBOM owners want advisory summaries) while the implementation reflects the provider's perspective (advisory service computes the data).

Alternatively, this route could be registered in `modules/fundamental/src/sbom/endpoints/mod.rs` if the codebase convention is to organize routes strictly by URL path rather than domain ownership. This would be determined during the Step 4 code inspection.
