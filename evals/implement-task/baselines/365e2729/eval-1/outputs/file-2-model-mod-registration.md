# File 2 (MODIFY): `modules/fundamental/src/advisory/model/mod.rs`

## Purpose
Register the new model module so `SeveritySummary` is reachable as
`crate::advisory::model::severity_summary::SeveritySummary`.

## Change
Add one line next to the existing module declarations, kept in alphabetical order:

```rust
pub mod details;
pub mod severity_summary;   // NEW
pub mod summary;
```

## Notes
- If the existing `mod.rs` re-exports its submodules (e.g. `pub use summary::*;`), add the
  matching `pub use severity_summary::*;` to stay consistent. This would be checked with
  `get_symbols_overview` before editing.
- No other changes.
