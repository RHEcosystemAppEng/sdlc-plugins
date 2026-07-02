# File 4: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from other parts of the crate.

## Detailed Changes

### Current State (expected)

```rust
pub mod summary;
pub mod details;
```

### Change

Add a new module declaration:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

### Specifics

- Add `pub mod severity_summary;` to the existing list of module declarations.
- This follows the existing pattern where each model struct has its own file and is registered in `mod.rs`.
- Placement: after the existing module declarations, maintaining alphabetical or logical ordering consistent with siblings.

### Conventions Followed

- Module declaration pattern matches existing `pub mod summary;` and `pub mod details;` lines.
- Public visibility (`pub mod`) to allow access from `endpoints/` and `service/` directories.
