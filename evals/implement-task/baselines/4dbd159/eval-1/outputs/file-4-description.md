# File 4: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Purpose

Register the new `severity_summary` model module so it is accessible from the advisory model namespace.

## Pre-Implementation Inspection

Before modifying, inspect the file using:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` to see existing module declarations

Expected current content (based on repo structure -- siblings `summary.rs` and `details.rs`):

```rust
pub mod details;
pub mod summary;
```

## Detailed Changes

Add one line to register the new module:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

### Design Decisions

- **Alphabetical ordering**: The new `pub mod severity_summary;` is inserted alphabetically between `details` and `summary`, following Rust convention for module declarations
- **Minimal change**: Only one line added -- no other modifications to this file
- **Follows sibling pattern**: Matches the existing `pub mod summary;` and `pub mod details;` declarations exactly
