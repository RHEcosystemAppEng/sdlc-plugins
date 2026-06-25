# File 4: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Purpose
Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the `advisory::model` module.

## Detailed Changes

Add a single line to the existing `mod.rs` file, alongside the existing module declarations:

### Addition

```rust
pub mod severity_summary;
```

This line should be added after the existing `pub mod summary;` and `pub mod details;` declarations, following alphabetical ordering if the existing modules are alphabetically ordered, or at the end of the module list otherwise.

### Expected State After Modification

The `mod.rs` file will contain (approximately):

```rust
pub mod details;
pub mod summary;
pub mod severity_summary;
```

## Conventions Applied
- **Module registration**: Matches the pattern of sibling `mod.rs` files that declare `pub mod` for each sub-module
- **Visibility**: Uses `pub mod` to export the struct for use in endpoints and service code
