# File 4: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from the `advisory::model` namespace.

## Current State (Expected)

The file currently contains re-exports for existing model modules:

```rust
pub mod details;
pub mod summary;
```

## Change

Add a single line to register the new module:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Detailed Diff

```diff
 pub mod details;
+pub mod severity_summary;
 pub mod summary;
```

## Design Decisions

- **Alphabetical ordering:** The new `pub mod` line is inserted in alphabetical order between `details` and `summary`, following Rust convention for module declarations.
- **No re-export:** The module is declared with `pub mod`, making `SeveritySummary` accessible as `advisory::model::severity_summary::SeveritySummary`. No `pub use` re-export is added at this level unless the existing codebase does so for sibling modules (to be confirmed at implementation time).
