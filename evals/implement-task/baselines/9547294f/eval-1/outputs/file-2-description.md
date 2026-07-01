# File 2: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so it is accessible from the advisory model namespace.

## Detailed Changes

Add a single line to the existing module declarations:

```rust
pub mod severity_summary;
```

This should be added alongside the existing `pub mod summary;` and `pub mod details;` declarations, maintaining alphabetical ordering if that is the existing convention, or appended after the last existing module declaration.

### Before (expected current state)

```rust
pub mod details;
pub mod summary;
```

### After

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Conventions Applied

- Module registration via `pub mod <name>;` in `mod.rs` -- standard Rust module pattern used throughout the codebase
- Alphabetical ordering of module declarations (if existing siblings follow this convention)
