# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so that `SeveritySummary` is accessible from the advisory model namespace.

## Pre-Implementation Inspection

Before modifying, would use `mcp__serena_backend__get_symbols_overview` on this file to see the current module declarations. Expect to find:

```rust
pub mod summary;
pub mod details;
```

## Changes

Add a single line to register the new module, placed alphabetically or after the existing module declarations to match the ordering pattern of siblings:

```rust
pub mod severity_summary;
```

The full file after modification would look like:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

(Or following whatever ordering convention the existing file uses -- alphabetical shown here as default.)

## Verification

- Confirm `pub mod severity_summary;` is added
- Confirm no other changes to this file
- Confirm the new module file `severity_summary.rs` exists in the same directory (File 4)
