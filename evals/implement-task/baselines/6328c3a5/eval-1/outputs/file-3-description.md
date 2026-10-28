# File 3: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Pre-implementation Inspection

Before modifying, would use Serena to inspect:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")` -- see existing module declarations
2. Read the file to confirm the pattern of `pub mod` declarations

## Changes

Add a single line to register the new model module:

```rust
pub mod severity_summary;
```

This should be added alongside the existing declarations:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;  // NEW
```

### Placement

Added alphabetically or after the last existing `pub mod` declaration, following whichever ordering convention is used in the file. If existing entries are in declaration order (not alphabetical), add at the end.

### Convention conformance

- Uses `pub mod` to re-export, matching sibling declarations
- Module name matches the file name (`severity_summary.rs`)
- snake_case naming consistent with all other module declarations
