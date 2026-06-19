# File 3: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory model.

## Detailed Changes

### Add module declaration

Add the following line alongside the existing `pub mod summary;` and `pub mod details;` declarations:

```rust
pub mod severity_summary;
```

## Conventions Followed

- Uses `pub mod` declaration consistent with existing model module registrations (`pub mod summary;`, `pub mod details;`)
- Module name matches the file name (`severity_summary.rs`)
- Placed in alphabetical or logical order with existing module declarations
