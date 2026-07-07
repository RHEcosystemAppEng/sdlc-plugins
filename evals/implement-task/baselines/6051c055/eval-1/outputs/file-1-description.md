# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose
Register the new `severity_summary` model module so it is accessible from the advisory model namespace.

## Changes

Add a single line to the existing module declarations:

```rust
pub mod severity_summary;
```

This line should be added in alphabetical order among the existing `pub mod` declarations in the file. For example, if the file currently contains:

```rust
pub mod details;
pub mod summary;
```

It becomes:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Rationale
Following the established pattern where each model struct lives in its own file and is registered via `pub mod` in the parent `mod.rs`. This is consistent with how `summary.rs` and other model files are registered.
