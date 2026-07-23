# File 1: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose
Register the new `severity_summary` model module so it is accessible to the service and endpoint layers.

## Changes

Add one line to the existing module declarations:

```rust
pub mod severity_summary;
```

This follows the existing pattern where `mod.rs` declares sibling modules. The file already contains:
```rust
pub mod summary;
pub mod details;
```

The new line should be added after the existing module declarations, maintaining alphabetical order or appending at the end (matching whichever convention the existing entries follow).

## Impact
- Exposes the `SeveritySummary` struct for use in `advisory::service::advisory.rs` and `advisory::endpoints::severity_summary.rs`
- No backward compatibility concerns -- purely additive
