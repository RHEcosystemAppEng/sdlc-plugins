# File 3: modules/fundamental/src/advisory/model/mod.rs

**Action**: Modify (existing file)

## Pre-Implementation Inspection

Before modifying, inspect this file using:
- Read or `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` to see existing `pub mod` declarations

## Changes

Add a single line to register the new model module:

```rust
pub mod severity_summary;
```

This follows the existing pattern in the file, which already contains declarations like:
```rust
pub mod summary;
pub mod details;
```

The new declaration should be added in alphabetical order relative to existing modules, or at the end of the list, following whichever convention the existing file uses.
