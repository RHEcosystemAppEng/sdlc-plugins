# File 1: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` submodule in the model barrel file so that other modules can import `SeveritySummary`.

## Current State

The file currently contains module declarations for existing models:

```rust
pub mod summary;
pub mod details;
```

## Changes

Add a new `pub mod` declaration for the `severity_summary` module, following the existing pattern of sibling module registrations:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

## Rationale

This follows the established convention where each model struct lives in its own file and is registered via `pub mod` in the parent `mod.rs`. The sibling modules `summary` and `details` follow this exact pattern.

## Impact

- Makes `SeveritySummary` accessible as `crate::advisory::model::severity_summary::SeveritySummary`
- No breaking changes to existing code
