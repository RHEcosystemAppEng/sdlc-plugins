# File 6: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Purpose
Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory model namespace.

## Reference Files to Inspect First
- `modules/fundamental/src/advisory/model/mod.rs` -- Read the existing module declarations to understand the pattern (e.g., `pub mod summary;`, `pub mod details;`).

## Changes

Add a single line to register the new model module, following the existing pattern of `pub mod` declarations:

```rust
pub mod severity_summary;
```

Place this line alongside the existing module declarations (e.g., near `pub mod summary;`), maintaining alphabetical ordering if that is the convention in the file.

## Notes
- This is a minimal, one-line change that follows the exact pattern of existing module registrations.
- The `pub` visibility is required so that the endpoint handler and service can import `SeveritySummary` from the model module.
- No other changes to this file are needed.
