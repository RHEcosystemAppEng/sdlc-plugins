# File 5: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose
Register the new `severity_summary` model module.

## Changes

Add module declaration:

```rust
// Existing:
pub mod summary;
pub mod details;

// Add:
pub mod severity_summary;
```

## Rationale
- Follows the existing module declaration pattern (`pub mod summary; pub mod details;`)
- Makes `SeveritySummary` struct accessible from other modules via `crate::advisory::model::severity_summary::SeveritySummary`
