# File 4: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from other parts of the codebase (service layer and endpoint handler).

## Detailed Changes

### Add module declaration

Add the following line to the existing module declarations in `modules/fundamental/src/advisory/model/mod.rs`:

```rust
pub mod severity_summary;
```

This line should be added in alphabetical order among the existing module declarations.

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

## Conventions Followed

- **Module registration**: Each model struct lives in its own file and is registered via `pub mod` in the parent `mod.rs`, consistent with the existing `summary` and `details` modules.
- **Alphabetical ordering**: Module declarations are kept in alphabetical order (`details`, `severity_summary`, `summary`), following standard Rust convention.
- **Public visibility**: Uses `pub mod` to make the struct accessible from the `endpoints` and `service` layers within the crate.
