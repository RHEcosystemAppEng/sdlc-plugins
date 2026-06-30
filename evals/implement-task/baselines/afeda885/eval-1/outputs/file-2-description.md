# File 2: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model sub-module so it is accessible from the advisory module.

## Detailed Changes

Add the following line to the existing `mod.rs` file, alongside the existing `pub mod summary;` and `pub mod details;` declarations:

```rust
pub mod severity_summary;
```

This should be placed in alphabetical order with the existing module declarations, or at the end of the `pub mod` block if no strict ordering is observed.

## Conventions Applied

- **Module registration**: Follows the standard Rust pattern of declaring sub-modules in the parent `mod.rs`
- **Sibling pattern**: Matches how `summary` and `details` modules are already registered in `model/mod.rs`
- **Minimal change**: Only one line added -- keeps the modification scoped
