# File 3: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory model namespace.

## Pre-Implementation Analysis

Before modifying, would use Serena to inspect:
- `mcp__serena_backend__get_symbols_overview` on this file to see existing `pub mod` declarations
- Confirm existing pattern: `pub mod summary;` and `pub mod details;` are already declared here

## Changes

### Add module re-export

Add a new `pub mod` declaration alongside the existing ones:

```rust
pub mod severity_summary;
```

This follows the existing pattern where `mod.rs` re-exports sub-modules (`pub mod summary;`, `pub mod details;`).

## Key Decisions

- **Visibility**: `pub mod` to match sibling declarations (`pub mod summary;`, `pub mod details;`)
- **Placement**: Added after existing module declarations, maintaining alphabetical order
- **Naming**: `severity_summary` matches the file name `severity_summary.rs`, following snake_case convention
