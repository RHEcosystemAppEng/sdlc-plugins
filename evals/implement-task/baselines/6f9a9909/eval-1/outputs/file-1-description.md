# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` sub-module so the `SeveritySummary` struct is
accessible from other parts of the crate.

## Current State

The file currently declares two public sub-modules:

```rust
pub mod summary;
pub mod details;
```

## Changes

Add a single line to register the new module:

```rust
pub mod severity_summary;
```

This follows the exact pattern of the existing `pub mod summary;` and `pub mod details;`
declarations. The new line should be added after the existing module declarations,
maintaining alphabetical or logical ordering consistent with the file.

## Rationale

Rust requires explicit module registration in `mod.rs` for the compiler to include
the new file. Without this line, `severity_summary.rs` would not be compiled or
accessible.
