# File 2: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose
Register the new `severity_summary` sub-module so the `SeveritySummary` struct is accessible from the advisory model module.

## Pre-implementation inspection
- Read `modules/fundamental/src/advisory/model/mod.rs` to see existing module registrations.
- Expected to find lines like:
  ```rust
  pub mod summary;
  pub mod details;
  ```

## Detailed Changes

### Add module registration

Add one line to the existing module declarations:

```rust
pub mod severity_summary;
```

This follows the exact pattern of existing `pub mod summary;` and `pub mod details;` declarations in the same file.

### Placement
- Add after the existing `pub mod` declarations, maintaining alphabetical order if that is the convention, or at the end of the `pub mod` block if siblings are not ordered.

### Conventions followed
- Uses `pub mod` declaration matching sibling pattern.
- Module name matches the filename (`severity_summary.rs`).
- Single-line addition, minimal change to existing file.
