# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model submodule so that the `SeveritySummary` struct is accessible from the advisory model namespace.

## Pre-Implementation Inspection

Before modifying, use `mcp__serena_backend__get_symbols_overview` on this file to see existing `pub mod` declarations. Expected to find:

```rust
pub mod summary;
pub mod details;
```

## Changes

Add a single line to register the new submodule:

```rust
pub mod severity_summary;
```

This follows the existing pattern of one `pub mod` declaration per model submodule. The new line should be added after the existing module declarations, maintaining alphabetical order if that is the established convention, or at the end if modules are listed in order of addition.

## Backward Compatibility

Use `mcp__serena_backend__find_referencing_symbols` on this module to confirm that adding a new `pub mod` does not conflict with existing wildcard re-exports or namespace collisions. The new module name `severity_summary` is unique and does not collide with `summary` or `details`.

## Convention Compliance

- Follows the triple-directory module structure pattern (model/service/endpoints)
- Uses snake_case module naming consistent with siblings (`summary`, `details`)
- Single `pub mod` declaration per submodule, no re-exports needed at this level
