# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so it is executed by the migration runner.

## Changes

### 1. Add module declaration

Add a new module declaration for the migration:

```rust
mod m0002_drop_advisory_status;
```

This is placed after the existing `mod m0001_initial;` declaration.

### 2. Register migration in the migrations() function

Add the new migration to the `vec![]` in the `migrations()` function, following the existing pattern:

**Before:**
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

## Patterns Followed

- **Module registration**: follows the same `Box::new(module::Migration)` pattern as `m0001_initial`
- **Ordering**: new migration appended after existing migrations to maintain chronological order
- **Module declaration**: placed alongside other migration module declarations
