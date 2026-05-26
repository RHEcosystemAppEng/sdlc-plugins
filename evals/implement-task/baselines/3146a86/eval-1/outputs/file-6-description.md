# File 6: MODIFY — `modules/fundamental/src/advisory/model/mod.rs`

## Purpose
Register the new `severity_summary` model module.

## Changes

Add module declaration:

```rust
pub mod severity_summary;
```

This follows the pattern of existing module registrations (`pub mod summary;`, `pub mod details;`) in the model mod.rs file.

## Conventions Applied

- Module declaration follows alphabetical ordering convention of existing `pub mod` declarations
- Matches the pattern seen in `modules/fundamental/src/advisory/model/mod.rs` for sibling modules
