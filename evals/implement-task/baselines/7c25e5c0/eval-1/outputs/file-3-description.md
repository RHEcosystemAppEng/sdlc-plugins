# File 3 — Modify: `modules/fundamental/src/advisory/model/mod.rs`

## What changes

Add `pub mod severity_summary;` to register the new model module.

## Code inspection

Before modifying, inspect with `mcp__serena_backend__get_symbols_overview` on `advisory/model/mod.rs` to see existing module registrations (`pub mod summary;`, `pub mod details;`).

## Detailed changes

Add at the bottom of the existing module declarations:

```rust
pub mod severity_summary;
```

This follows the same pattern as the existing `pub mod summary;` and `pub mod details;` declarations.
