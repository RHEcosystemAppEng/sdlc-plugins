# File 2: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose
Register the new `severity_summary` model module so it is accessible from the advisory module.

## Detailed Changes

Add a single line to the existing `mod.rs`:

```rust
pub mod severity_summary;
```

This should be added alongside the existing module declarations (`pub mod summary;`, `pub mod details;`), in alphabetical order.

## Rationale
- Follows the module registration pattern used by all sibling model directories
- Without this line, the `SeveritySummary` struct would not be reachable from other modules
