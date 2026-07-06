# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary route in the advisory module's endpoint router.

## Detailed Changes

### Add module declaration

At the top of the file, alongside existing module declarations (`mod get;`, `mod list;`),
add:

```rust
mod severity_summary;
```

### Add route registration

In the router builder function (where existing routes like
`Router::new().route("/api/v2/advisory", get(list::handler))` are registered),
add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Placement

The new `.route(...)` call should be appended after the existing route registrations
in the router chain, following the pattern of how `get.rs` and `list.rs` handlers
are registered.

### Design decisions

- **Route path `/api/v2/sbom/:id/advisory-summary`**: matches the API specification
  in the task description. The path is under `/sbom/{id}/` since the summary is
  scoped to an SBOM, even though the handler lives in the advisory module. This
  is appropriate because the advisory module owns the aggregation logic.
- **`:id` path parameter**: Axum uses `:id` syntax for path parameters (some versions
  use `{id}`; match whichever the existing routes in this file use).
- **`get(...)` method**: the endpoint is read-only, so it uses the GET method handler.

### Conventions followed

- Module declaration follows alphabetical or existing ordering convention in the file.
- Route registration follows the `.route(path, method(handler))` chaining pattern.
- Handler function is referenced by module path: `severity_summary::get_severity_summary`.
