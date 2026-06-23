# File 3: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Change Type
Modify existing file

## Description
Add `pub mod severity_summary;` to register the new model module so the `SeveritySummary` struct is accessible from the advisory model namespace.

## Detailed Changes

### Add module declaration

Add the following line alongside existing module declarations (`pub mod summary;`, `pub mod details;`):

```rust
pub mod severity_summary;
```

This registers the new `severity_summary.rs` file as a sub-module of the advisory model module, making `SeveritySummary` available as `crate::advisory::model::severity_summary::SeveritySummary`.

## Conventions Followed
- Module declaration pattern matches existing `pub mod summary;` and `pub mod details;` declarations
- Module name uses snake_case matching the file name
- Placed in logical order alongside sibling module declarations
