# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory model hierarchy.

## Pre-Modification Inspection

Before making changes, inspect via Serena or Read:
1. Read the file to see existing module declarations
2. Confirm the pattern: `pub mod summary;` and `pub mod details;` are already declared

## Detailed Changes

### Add module declaration

Add `pub mod severity_summary;` alongside the existing module declarations:

```rust
pub mod details;
pub mod summary;
pub mod severity_summary;  // NEW
```

### Design Decisions

- **Single-line change**: this file only needs one new line to register the module
- **Module naming**: `severity_summary` matches the file name `severity_summary.rs`
- **Ordering**: placed after existing declarations, or alphabetically if that is the convention (determined by inspecting the current file)

### Convention Compliance

- Follows the exact `pub mod <name>;` pattern used for sibling modules (`summary`, `details`)
- Module name uses snake_case matching Rust conventions
