# File 3: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Pre-implementation Inspection

Before modifying, would use Serena to understand the current state:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")` -- see existing module declarations.
2. Read the file to see the full content (typically short -- just `pub mod` lines).

## Changes

### Add module declaration for the new model

Add a new `pub mod` line alongside existing declarations:

```rust
pub mod severity_summary;
```

**Placement**: After existing module declarations (`pub mod summary;`, `pub mod details;`), in alphabetical order or following the existing ordering convention.

## Rationale

- Follows the same pattern as existing module declarations in this file (`pub mod summary;`, `pub mod details;`).
- The `pub` visibility is required so the endpoint handler and service can import `SeveritySummary` from outside the model module.
- This is a minimal change -- a single line addition.
