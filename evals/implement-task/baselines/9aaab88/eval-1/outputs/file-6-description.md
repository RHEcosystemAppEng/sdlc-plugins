# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module so that `SeveritySummary` is accessible from `crate::advisory::model::severity_summary`.

## Sibling Reference

Follows the existing pattern in this file, which declares `pub mod` for each model submodule:

```rust
// Existing:
pub mod summary;
pub mod details;
```

## Detailed Changes

Add the following line alongside existing module declarations:

```rust
pub mod severity_summary;
```

The line should be placed in alphabetical order relative to the existing module declarations, or at the end if the existing declarations don't follow alphabetical ordering:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Key Design Decisions

- **`pub mod`**: Uses `pub mod` (not `mod`) to make the module publicly accessible, matching the pattern of `summary` and `details` modules.
- **Ordering**: Follows whatever ordering convention (alphabetical or logical) the existing declarations use in this file.
- **No re-export**: Does not add a `pub use severity_summary::SeveritySummary;` re-export unless the sibling modules (`summary.rs`, `details.rs`) have such re-exports. The import path `crate::advisory::model::severity_summary::SeveritySummary` is acceptable and consistent with how other model types are referenced.
