# File 3: Modify `modules/fundamental/src/advisory/model/mod.rs`

**Action:** Modify (register new model module)

## Pre-implementation inspection

Before modifying this file, read it to see the existing module declarations (e.g., `pub mod summary;`, `pub mod details;`).

## Changes

Add the new model module declaration:

```rust
pub mod severity_summary;
```

This registers the `SeveritySummary` struct defined in `severity_summary.rs` so it can be imported by the service and endpoint modules.

**Pattern conformance:**
- Follows the existing pattern of `pub mod <name>;` declarations in `model/mod.rs`
- Placement: add after the existing `pub mod details;` or `pub mod summary;` lines, maintaining alphabetical or logical ordering consistent with sibling entries
