# File 2: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Action: MODIFY

## Purpose

Register the new `severity_summary` module so the `SeveritySummary` struct is accessible from the advisory model.

## Detailed Changes

Add a new `pub mod` declaration to register the severity_summary module. Following the existing pattern in this file (which already has `pub mod summary;` and `pub mod details;`):

```rust
// Add after existing module declarations:
pub mod severity_summary;
```

This makes `SeveritySummary` accessible as `crate::advisory::model::severity_summary::SeveritySummary` from within the fundamental module.

## Conventions Applied

- **Module registration**: follows the same `pub mod <name>;` pattern used for `summary` and `details` modules.
- **Alphabetical ordering**: if existing modules are listed alphabetically, insert `severity_summary` in the appropriate position.
