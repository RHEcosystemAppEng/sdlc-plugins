# File 2: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` submodule so it is accessible from the `advisory::model` module.

## Current State

The file currently contains module registrations for existing model types:

```rust
pub mod details;
pub mod summary;
```

## Changes

Add a single line to register the new module:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

### Details

- Add `pub mod severity_summary;` in alphabetical order among the existing module declarations.
- This follows the existing pattern where `pub mod summary;` and `pub mod details;` are already registered.
- No other changes to this file.

### Sibling Parity

Matches the pattern in `sbom/model/mod.rs` and `package/model/mod.rs` where each model submodule is registered with a `pub mod` declaration.
