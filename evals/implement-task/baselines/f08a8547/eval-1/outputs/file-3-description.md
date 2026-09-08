# File 3: Route Registration

**File**: `modules/fundamental/src/advisory/endpoints/mod.rs`
**Action**: MODIFY

## Current State

This file registers routes for the advisory module. Based on sibling patterns
(e.g., `sbom/endpoints/mod.rs`), it follows the Axum router pattern:

```rust
mod list;
mod get;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
}
```

## Changes

### 1. Add module import for the new handler

```rust
mod list;
mod get;
mod severity_summary;
```

### 2. Add route registration

Add the new route to the router chain. The endpoint is scoped under `/api/v2/sbom/{id}/`
because it aggregates advisories *for a specific SBOM*, not advisories in general:

```rust
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::get_severity_summary),
        )
}
```

## Design Note: Route Placement

The endpoint path `/api/v2/sbom/{id}/advisory-summary` is semantically an SBOM
sub-resource (it answers "what are the advisory severities for this SBOM?"). It is
registered in the advisory module's router because:
1. The service logic lives in `AdvisoryService`
2. The model struct is in the advisory model module
3. The implementation notes explicitly say to register it in the advisory endpoints

If the project prefers SBOM-scoped endpoints to live in the SBOM module, this
would be flagged during scope containment review. For now, the task description
is followed as written.

## Convention Adherence

- Follows the `Router::new().route()` chaining pattern from siblings.
- Uses Axum's `:id` path parameter syntax (consistent with existing routes).
- Module import follows `mod <name>;` pattern at the top of the file.
