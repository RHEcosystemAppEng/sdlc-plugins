# File 3: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model submodule so it is accessible from the rest of the crate.

## Detailed Changes

Add a single line to the existing module declarations:

```rust
pub mod severity_summary;
```

This line would be added alongside the existing `pub mod summary;` and `pub mod details;` declarations, maintaining alphabetical order if that is the convention in the file.

## Inspection before modification

Use `mcp__serena_backend__get_symbols_overview` on this file to see existing module declarations. Confirm the pattern of `pub mod <name>;` lines. Place the new declaration in the appropriate position.

## Conventions followed

- Matches the existing pattern of `pub mod` declarations in this file
- Module name matches the file name (`severity_summary` for `severity_summary.rs`)
