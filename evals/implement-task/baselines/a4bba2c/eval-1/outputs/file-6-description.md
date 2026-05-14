# File 6: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Expose the new `severity_summary` model module so that the `SeveritySummary` struct can be imported by the service layer and endpoint handler. This follows the pattern used for existing model sub-modules like `summary` and `details`.

## Sibling Reference

- Current contents of `modules/fundamental/src/advisory/model/mod.rs` — existing module declarations for `pub mod summary;` and `pub mod details;`
- `modules/fundamental/src/sbom/model/mod.rs` — sibling module for cross-reference

## Changes

Add a single line to the existing module declarations:

```rust
pub mod severity_summary;
```

## Example of modified file

```rust
pub mod details;
pub mod summary;
pub mod severity_summary;
```

## Conventions Followed

- `pub mod` visibility matches existing model module declarations (`pub mod summary;`, `pub mod details;`) — models are public so they can be imported by service and endpoint layers
- Module name matches the file name (`severity_summary.rs` -> `pub mod severity_summary;`)
- Placement after existing declarations — follows append-at-end convention

## Notes

- This is a minimal one-line change
- The ordering (alphabetical vs declaration order) should be confirmed by inspecting the actual file during pre-implementation analysis
