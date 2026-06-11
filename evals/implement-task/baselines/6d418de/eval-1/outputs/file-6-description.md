# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action:** MODIFY

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from the advisory model namespace.

## Detailed Changes

### Add module declaration

Add the following line alongside existing module declarations:

```rust
pub mod severity_summary;
```

### Before (conceptual):

```rust
pub mod summary;
pub mod details;
```

### After (conceptual):

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

### Design rationale

- **Module registration pattern:** Follows the exact pattern used by existing model sub-modules (`summary`, `details`). Each model struct lives in its own file and is registered via `pub mod` in `mod.rs`.
- **Minimal change:** Single line addition, no other modifications needed. This makes the `SeveritySummary` struct importable as `crate::advisory::model::severity_summary::SeveritySummary`.

### Conventions followed

- `pub mod <name>;` declaration pattern matching siblings.
- Alphabetical or logical ordering consistent with existing declarations.
