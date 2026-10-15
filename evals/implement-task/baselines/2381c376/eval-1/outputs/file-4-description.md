# File 4: modules/fundamental/src/advisory/model/mod.rs

## Operation: MODIFY

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from `crate::advisory::model::severity_summary::SeveritySummary`.

## Sibling Reference

This file already contains `pub mod summary;` and `pub mod details;` for the existing model modules.

## Detailed Changes

### Add module declaration

Add the following line alongside the existing module declarations:

```rust
pub mod severity_summary;
```

### Before (existing content, approximate)

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

## Design Decisions

- **Alphabetical ordering**: Module declarations are added in alphabetical order to match conventions (if siblings follow alphabetical order; otherwise, append at end).
- **Minimal change**: Only a single line is added to register the new module. No other modifications to this file.

## Conventions Applied

- `pub mod <name>;` pattern matching existing sibling module registrations
- snake_case module name matching the file name (`severity_summary`)
