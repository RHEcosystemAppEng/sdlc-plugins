# File 4 -- MODIFY: modules/fundamental/src/advisory/model/mod.rs

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory model namespace.

## Conventions Applied

- **Module registration:** Follows the existing pattern where each model file is registered as `pub mod <name>;` in the parent `mod.rs`. Siblings `summary` and `details` are already registered this way.

## Detailed Changes

Add one line to register the new module. The existing file likely contains:

```rust
pub mod details;
pub mod summary;
```

Add the new module registration:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

The new line `pub mod severity_summary;` is inserted in alphabetical order among the existing module declarations, following Rust convention for module ordering.

## Scope

This is a minimal one-line addition. No other changes to this file.
