# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action:** MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory endpoints module.

## Detailed Changes

### Add module declaration

Add at the top of the file alongside existing module declarations:

```rust
pub mod severity_summary;
```

### Add route registration

In the route registration section (where `Router::new()` chains `.route(...)` calls), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Import

Add the import for the `get` method from axum if not already present:

```rust
use axum::routing::get;
```

### Before (conceptual):

```rust
pub mod list;
pub mod get;

// ... route registration ...
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
```

### After (conceptual):

```rust
pub mod list;
pub mod get;
pub mod severity_summary;

// ... route registration ...
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Design rationale

- **Route registration pattern:** Follows the existing pattern of `.route()` chaining in `endpoints/mod.rs`, consistent with how `list.rs` and `get.rs` endpoints are registered.
- **Endpoint path:** Uses `/api/v2/sbom/:id/advisory-summary` as specified in the task's API Changes section. The path is under the SBOM namespace since it queries advisories for a specific SBOM.
- **Module declaration:** `pub mod severity_summary;` follows the same pattern as `pub mod list;` and `pub mod get;`.
- **Auto-mounting:** No changes needed to `server/src/main.rs` since the server auto-mounts routes from module registration, as confirmed by the task description.

### Conventions followed

- Route added by appending a `.route()` call to the existing router chain.
- Module declared with `pub mod` at the file top.
- Handler referenced as `module::function_name` pattern.
