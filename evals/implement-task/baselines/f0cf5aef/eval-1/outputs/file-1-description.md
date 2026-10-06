# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model sub-module so the `SeveritySummary` struct
is accessible from the `advisory::model` namespace.

## Pre-implementation inspection

Before modifying, inspect the file using:
```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")
```

Confirm the existing pattern of `pub mod` declarations (expecting `pub mod summary;`
and `pub mod details;`).

## Changes

Add a single line:

```rust
pub mod severity_summary;
```

This follows the alphabetical or logical ordering of existing `pub mod` declarations.
Place it after the existing `pub mod summary;` line to keep related modules adjacent.

## Convention conformance

- Matches the existing pattern in this file: one `pub mod` line per model sub-module
- Module name `severity_summary` follows the snake_case naming convention observed in siblings (`summary`, `details`)
