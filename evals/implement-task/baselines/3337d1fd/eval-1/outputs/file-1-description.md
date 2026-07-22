# File 1: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose
Register the new `severity_summary` model sub-module so it is compiled and publicly accessible.

## Changes

Add one line to the existing module declarations:

```rust
pub mod severity_summary;
```

This line should be added alongside the existing `pub mod summary;` and `pub mod details;` declarations, maintaining alphabetical order (after `details`, before or after `summary` depending on current ordering).

## Rationale
Follows the established convention: every model type has its own file under `model/` and is registered in `model/mod.rs` via `pub mod`. This mirrors how `summary.rs` and `details.rs` are already registered.
