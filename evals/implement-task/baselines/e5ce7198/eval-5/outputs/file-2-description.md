# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so SeaORM's migration runner picks it up.

## Pre-Implementation Inspection

Before modifying this file, inspect:
- `migration/src/lib.rs` -- to understand the current module declarations, the `migrations()` function structure, and the exact pattern for adding new migrations to the vec.

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, following the existing `m0001_initial` declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial` entry:

```rust
// Before:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}

// After:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Key Design Decisions

1. **Ordering**: The new migration is appended after `m0001_initial` to maintain chronological ordering. The `m0002_` prefix ensures correct sorting.
2. **Module path**: Uses `m0002_drop_advisory_status::Migration` matching the struct name exported from the new module.

## Sibling Parity Check (Constraint 5.8)

The registration pattern exactly mirrors how `m0001_initial` is registered: same `mod` declaration style, same `Box::new(...)` wrapping in the migrations vec.
