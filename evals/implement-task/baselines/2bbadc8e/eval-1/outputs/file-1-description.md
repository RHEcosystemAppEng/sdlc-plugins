# File 1: modules/fundamental/src/advisory/model/mod.rs

**Action**: Modify (existing file)

## Purpose

Register the new `severity_summary` model sub-module so the `SeveritySummary` struct is accessible from the `advisory::model` namespace.

## Changes

Add a single line to register the new module:

```rust
pub mod severity_summary;
```

This follows the existing pattern in the file where sibling modules like `summary` and `details` are already declared:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;  // NEW
```

## Rationale

The module pattern in this project requires explicit `pub mod` declarations in `mod.rs` for each sub-module. Without this line, the `SeveritySummary` struct defined in `severity_summary.rs` would not be visible to the service or endpoint layers.

## Convention Conformance

- Follows the `pub mod <name>;` registration pattern used by sibling modules (`summary`, `details`)
- File ordering: added after existing module declarations alphabetically or at the end
