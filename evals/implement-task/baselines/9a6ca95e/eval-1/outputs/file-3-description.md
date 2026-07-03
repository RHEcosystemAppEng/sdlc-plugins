# File 3: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Inspection performed

Used `mcp__serena_backend__get_symbols_overview` on this file to see the existing module registrations. Inspected sibling model `mod.rs` files (e.g., `modules/fundamental/src/sbom/model/mod.rs`) for comparison.

## Current state

The file registers existing model submodules:

```rust
pub mod details;
pub mod summary;
```

Each module declaration is followed by a re-export (`pub use`) in some cases.

## Changes

Add the new model module declaration:

```rust
pub mod severity_summary;
```

And add the corresponding re-export:

```rust
pub use severity_summary::*;
```

The full modified file would look like:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;

pub use details::*;
pub use severity_summary::*;
pub use summary::*;
```

(If the current file does not use `pub use` re-exports, omit those lines and keep only `pub mod severity_summary;`. Match whatever pattern is established.)

## Rationale

- Module declaration is inserted in alphabetical order, consistent with how `details` and `summary` are ordered
- Re-export follows the same pattern as sibling modules (if present), making `SeveritySummary` available as `crate::advisory::model::SeveritySummary`
