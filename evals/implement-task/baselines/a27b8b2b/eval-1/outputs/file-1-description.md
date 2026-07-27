# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model sub-module so it is accessible from the rest of the crate.

## Pre-implementation inspection

Before modifying, inspect this file using `mcp__serena_backend__get_symbols_overview` to see the current list of `pub mod` declarations. Confirm the pattern used to register sibling modules like `summary` and `details`.

## Changes

Add a single line to register the new module. Place it alphabetically among the existing module declarations:

```rust
// Existing lines (do not modify):
pub mod details;
pub mod summary;

// Add this line:
pub mod severity_summary;
```

## Rationale

This follows the existing pattern in the file where each model sub-module is declared via `pub mod`. The `severity_summary` module defined in `severity_summary.rs` (File 4) will be accessible as `crate::advisory::model::severity_summary::SeveritySummary`.

## Conventions applied

- Module registration pattern: `pub mod <name>;` in the parent `mod.rs`
- Alphabetical ordering of module declarations (matching sibling pattern)
