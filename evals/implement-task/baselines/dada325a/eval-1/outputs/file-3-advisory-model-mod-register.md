# File 3 (MODIFY): `modules/fundamental/src/advisory/model/mod.rs`

## Purpose
Register the new model module.

## Change
```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```
Modules are kept in alphabetical order to match the existing list. If siblings re-export (`pub use summary::*;`),
add `pub use severity_summary::*;` the same way. Otherwise the declaration is the only change.
