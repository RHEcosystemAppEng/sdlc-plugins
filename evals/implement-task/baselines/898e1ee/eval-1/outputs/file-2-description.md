# File 2: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so it is accessible from the `advisory::model` namespace.

## Sibling files inspected

- `modules/fundamental/src/advisory/model/mod.rs` (current state) -- contains `pub mod summary;` and `pub mod details;`
- `modules/fundamental/src/sbom/model/mod.rs` -- follows same pattern of `pub mod <name>;` declarations

## Conventions applied

- Module registration uses `pub mod <name>;` in `mod.rs` (consistent with existing entries)
- Alphabetical ordering of module declarations (matching sibling patterns)

## Detailed changes

Add one line to the existing `mod.rs`:

```rust
// Existing lines:
pub mod details;
pub mod summary;

// Add:
pub mod severity_summary;
```

The new `pub mod severity_summary;` line registers the `severity_summary.rs` file, making `SeveritySummary` accessible as `advisory::model::severity_summary::SeveritySummary`.

## Rationale

- This is the standard module registration pattern used throughout the codebase.
- Without this line, the new `severity_summary.rs` file would not be compiled or accessible.
