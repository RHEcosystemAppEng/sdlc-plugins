# File 3: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Action: MODIFY

## Purpose
Register the new `severity_summary` module so it is visible to the rest of the crate.

## Conventions Applied
- Module registration via `pub mod <name>;` in the parent `mod.rs` (sibling pattern from existing `pub mod summary;` and `pub mod details;` declarations)
- Alphabetical ordering of module declarations (if existing modules are alphabetically ordered)

## Detailed Changes

Add the following line to the existing module declarations in `modules/fundamental/src/advisory/model/mod.rs`:

```rust
pub mod severity_summary;
```

This should be added alongside the existing `pub mod summary;` and `pub mod details;` declarations. If the modules are listed alphabetically, insert it between `details` and `summary`:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Rationale
- This is the standard Rust module registration pattern used consistently across the codebase
- Without this declaration, the `SeveritySummary` type would not be accessible from the service or endpoint modules
- The change is minimal and follows the exact pattern of existing sibling declarations
