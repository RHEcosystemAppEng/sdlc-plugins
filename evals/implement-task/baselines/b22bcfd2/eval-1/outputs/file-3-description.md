# File 3: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so it is accessible from the advisory module.

## Pre-Implementation Inspection

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` to see existing module registrations
- Verify the pattern: expect to see `pub mod summary;` and `pub mod details;` already present

## Detailed Changes

Add a new line to register the severity_summary module, following the pattern of existing module declarations:

```rust
// Existing lines:
pub mod details;
pub mod summary;

// Add:
pub mod severity_summary;
```

The new `pub mod severity_summary;` line should be placed in alphabetical order among the existing module declarations (after `details`, before or after `summary` depending on exact sort order).

## Notes

- This is a one-line addition following the exact pattern of existing module registrations
- Alphabetical ordering matches Rust convention for module declarations
