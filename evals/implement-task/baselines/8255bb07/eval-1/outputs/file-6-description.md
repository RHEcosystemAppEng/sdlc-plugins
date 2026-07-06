# File 6: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from within the advisory module and by the endpoint handler.

## Pre-Implementation Inspection

Before modifying this file, inspect:
- **`modules/fundamental/src/advisory/model/mod.rs`** — Read the current module registration to see existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`) and understand the ordering convention.
- **`modules/fundamental/src/sbom/model/mod.rs`** — Sibling model `mod.rs` for additional pattern confirmation.

## Changes

Add the following line to the existing `pub mod` declarations:

```rust
pub mod severity_summary;
```

This should be placed alongside the existing module declarations (e.g., after `pub mod summary;` and `pub mod details;`), maintaining alphabetical order if that is the established convention, or at the end of the list otherwise.

## Conventions Applied

- **Module registration**: Uses `pub mod severity_summary;` matching the pattern of `pub mod summary;` and `pub mod details;` in the same file.
- **Visibility**: Uses `pub mod` to make the module publicly accessible, consistent with existing model module declarations.
- **Naming**: Module name `severity_summary` matches the file name `severity_summary.rs`, following Rust module conventions.
