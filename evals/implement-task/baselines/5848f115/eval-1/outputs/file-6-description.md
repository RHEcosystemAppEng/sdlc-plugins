# File 6: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model submodule so the `SeveritySummary` struct is accessible from the advisory model namespace.

## Pre-implementation analysis

Before modifying this file:
- Read the file via Read or `mcp__serena_backend__get_symbols_overview` to see the existing `pub mod` declarations.
- Confirm the pattern: expect to see `pub mod summary;` and `pub mod details;` already present.
- Cross-reference with `modules/fundamental/src/sbom/model/mod.rs` via Read to confirm the same pattern is used across modules.

## Detailed changes

Add a single line to the file, following the existing `pub mod` declarations:

```rust
pub mod severity_summary;
```

This should be placed alphabetically among the existing module declarations (after `pub mod details;`, before or after `pub mod summary;` depending on alphabetical ordering convention).

## Conventions applied

- Uses `pub mod` to publicly export the submodule, matching `pub mod summary;` and `pub mod details;` declarations
- Follows alphabetical ordering of module declarations (if that is the observed convention in the file)
- Single-line change -- minimal scope, no risk of side effects
