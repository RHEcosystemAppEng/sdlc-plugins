# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose
Register the new `severity_summary` endpoint module and add its route to the advisory router.

## Detailed Changes

### 1. Add module declaration

Add alongside existing module declarations:

```rust
pub mod severity_summary;
```

### 2. Add route registration

In the router construction function (where other routes like `get.rs` and `list.rs` are registered), add:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This should be added alongside the existing route registrations following the `Router::new().route(...)` pattern.

### 3. Add import (if not already glob-imported)

If the module uses explicit imports for handler functions:

```rust
use severity_summary::get_severity_summary;
```

## Rationale
- Follows the existing route registration pattern in `endpoints/mod.rs`
- The route path `/api/v2/sbom/:id/advisory-summary` matches the API contract in the task description
- Uses Axum's `get()` method handler, consistent with sibling GET endpoint registrations
- Note: the route is registered under the advisory module's router even though the path is under `/sbom/` — this is acceptable as the advisory module owns the aggregation logic
