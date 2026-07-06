# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route by importing the new handler module and adding the route to the existing router configuration.

## Pre-Implementation Inspection

Before modifying this file, inspect:
- **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Read the current route registration to understand the pattern: how `mod` declarations are organized, how `Router::new().route(...)` calls are chained, and the import structure.
- **`modules/fundamental/src/sbom/endpoints/mod.rs`** — Sibling endpoint registration file for additional pattern confirmation.

## Changes

### 1. Add module declaration

Add the new module declaration alongside existing ones (e.g., near `mod get;` and `mod list;`):

```rust
mod severity_summary;
```

### 2. Register the route

Add the new route to the `Router` builder, following the pattern of existing route registrations:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))
```

This should be added within the existing `Router::new()` chain alongside the other `.route(...)` calls.

## Conventions Applied

- **Module declaration**: Uses `mod severity_summary;` matching the pattern of `mod get;` and `mod list;` in the same file.
- **Route registration**: Uses `.route("/path", get(handler))` pattern matching existing registrations in this file.
- **Path convention**: Uses `:id` for Axum path parameters, matching existing route paths.
- **Handler reference**: References `severity_summary::handler` matching how other handlers are referenced (e.g., `get::handler`, `list::handler`).
