# File 3: `modules/fundamental/src/advisory/model/mod.rs`

**Action**: Modify existing file

## Purpose

Register the new `severity_summary` module so that the `SeveritySummary` struct is accessible from the `advisory::model` module path.

## Conventions Applied

- **Module registration pattern**: Follows the existing pattern in this file where sibling modules (`summary`, `details`) are declared with `pub mod`.
- **Alphabetical ordering**: If existing modules are alphabetically ordered, insert `severity_summary` in the correct position.

## Detailed Changes

Add the following line to `modules/fundamental/src/advisory/model/mod.rs`:

```rust
pub mod severity_summary;
```

### Before (existing content, representative):

```rust
pub mod details;
pub mod summary;
```

### After:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Design Decisions

- **Alphabetical insertion**: Placed between `details` and `summary` alphabetically, following the convention if existing modules are sorted. If they are not sorted, append at the end instead.
- **`pub mod`**: Public visibility to allow the endpoint handler and service to import `SeveritySummary` from the model module.
