# File 6: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory model namespace.

## Detailed Changes

Add the following line alongside the existing module declarations (near `pub mod summary;` and `pub mod details;`):

```rust
pub mod severity_summary;
```

This single line registers the new `severity_summary.rs` file as a submodule, making `SeveritySummary` accessible via `crate::advisory::model::severity_summary::SeveritySummary`.

## Conventions Followed

- **Module registration pattern**: follows the exact pattern used by `pub mod summary;` and `pub mod details;` in the same file.
- **Alphabetical ordering**: if the existing module declarations are alphabetically ordered, `severity_summary` would be placed after `summary` (or between `details` and `summary` depending on the existing order).
- **No additional changes**: no re-exports or use statements needed — the module is accessed via its full path, consistent with how `summary` and `details` are used.
