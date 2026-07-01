# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration registry so it is discovered and executed by the migration runner.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module, following the pattern of the existing `m0001_initial` module declaration.

**Before:**
```rust
mod m0001_initial;
```

**After:**
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the pattern of `m0001_initial`.

**Before (example based on sibling pattern):**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

### Design Decisions

1. **Ordering**: The new migration is appended after `m0001_initial` in the `vec![]`, preserving chronological ordering. Migrations must be registered in order since the migration runner executes them sequentially.

2. **Module naming**: The module name `m0002_drop_advisory_status` follows the existing naming convention of `m<sequence_number>_<description>`, incrementing from `m0001` to `m0002`.

3. **Registration pattern**: Uses `Box::new(m0002_drop_advisory_status::Migration)` to match the boxing pattern used for `m0001_initial::Migration`.

### Conventions Applied

- Module declaration placement follows alphabetical/sequential ordering after existing modules
- Migration registration uses the same `Box::new()` wrapping pattern as sibling entries
- Trailing comma after the last entry in the `vec![]` macro (Rust convention for easier diffs)
