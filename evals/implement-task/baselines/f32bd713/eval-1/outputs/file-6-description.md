# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action**: Modify

## Purpose

Register the new `severity_summary` model submodule so that the `SeveritySummary` struct
is accessible from the advisory model namespace.

## Pre-implementation inspection

Before modifying this file, would inspect using Serena:

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- see existing module declarations (`pub mod summary;`, `pub mod details;`)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/model/mod.rs` -- cross-reference with sibling model module for declaration pattern consistency

## Detailed changes

Add a single line to the existing module declarations:

```rust
pub mod severity_summary;
```

This line would be placed alongside the existing `pub mod summary;` and `pub mod details;`
declarations, in alphabetical order or following the existing ordering convention.

## Conventions applied

- `pub mod` declaration matching the existing `pub mod summary;` and `pub mod details;` pattern
- Module name matches the file name (`severity_summary.rs` -> `pub mod severity_summary;`)
- Follows the established module registration pattern where each model submodule is declared in `model/mod.rs`

## Notes

- This is a minimal, mechanical change -- adding one line to register the new module
- No re-exports needed unless the sibling pattern uses `pub use` to flatten the namespace (would be confirmed from inspection of the existing `mod.rs`)
