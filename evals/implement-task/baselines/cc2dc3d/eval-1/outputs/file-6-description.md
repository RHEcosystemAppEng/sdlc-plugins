# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action**: Modify existing file

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from the `advisory::model` namespace.

## Detailed Changes

Add the following line alongside existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`):

```rust
pub mod severity_summary;
```

## Conventions Applied

- **Module declaration**: follows the existing pattern in `model/mod.rs` where each model struct file is declared with `pub mod <name>;`
- **Ordering**: would be placed alphabetically among sibling declarations, or at the end, matching whichever pattern the existing file uses
- **Visibility**: uses `pub mod` to make the struct accessible from outside the model module, consistent with sibling declarations

## Notes

- This is a minimal one-line change that enables the rest of the codebase to import `SeveritySummary` via `crate::advisory::model::severity_summary::SeveritySummary`
