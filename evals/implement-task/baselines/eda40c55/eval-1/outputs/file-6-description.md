# File 6: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model module so its `SeveritySummary` struct
is accessible from the advisory model namespace.

## Detailed Changes

### Add module declaration

Add the following line alongside existing module declarations (`pub mod summary;`,
`pub mod details;`):

```rust
pub mod severity_summary;
```

### Placement

The new `pub mod` declaration should be placed in alphabetical order relative to
the existing declarations, or at the end if the existing declarations do not follow
alphabetical order. Based on siblings:

```rust
pub mod details;
pub mod severity_summary;  // NEW
pub mod summary;
```

### Design decisions

- **`pub mod`**: the module must be public so the endpoint handler can import
  `SeveritySummary` from `crate::advisory::model::severity_summary::SeveritySummary`.
- **Separate file, not inline**: follows the sibling pattern where each model struct
  gets its own file (`summary.rs`, `details.rs`).

### Conventions followed

- Module declaration uses `pub mod` matching siblings.
- File-per-struct pattern consistent with `summary.rs` and `details.rs`.
