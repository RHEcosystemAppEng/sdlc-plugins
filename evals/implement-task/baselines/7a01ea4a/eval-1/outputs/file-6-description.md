# File 6: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model sub-module so that the `SeveritySummary` struct is accessible from the advisory model hierarchy.

## Pre-implementation inspection

Before modifying this file, perform the following inspections:

- **`modules/fundamental/src/advisory/model/mod.rs`** -- Use `mcp__serena_backend__get_symbols_overview` (or Read tool) to see the existing module declarations. Expect to find lines like:
  ```rust
  pub mod summary;
  pub mod details;
  ```
- **`modules/fundamental/src/sbom/model/mod.rs`** -- Read as a sibling to confirm the `pub mod` declaration pattern is consistent.

## Detailed changes

Add the following line alongside existing module declarations:

```rust
pub mod severity_summary;
```

This should be placed in alphabetical order relative to existing declarations (after `pub mod details;` and before or after `pub mod summary;` depending on the existing order).

## Conventions followed

- Uses `pub mod` for public visibility, matching existing declarations
- Follows alphabetical ordering convention for module declarations
- Single-line declaration, no additional re-exports needed
