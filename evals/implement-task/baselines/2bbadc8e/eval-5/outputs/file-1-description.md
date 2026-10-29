# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's
migration runner discovers and executes it.

## Current State (Expected)

The file currently declares the `m0001_initial` module and returns it in a
`migrations()` function, following the standard SeaORM migration pattern:

```rust
mod m0001_initial;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m0001_initial::Migration),
        ]
    }
}
```

## Changes

### 1. Add module declaration

Add a `mod` declaration for the new migration module, placed after the existing
`m0001_initial` declaration to maintain chronological ordering:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### 2. Register the migration

Append the new migration to the `vec![]` in the `migrations()` function:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Rationale

- Ordering matters: migrations run in the order they appear in the vector.
  `m0002` must come after `m0001` to ensure the table exists before we alter it.
- Follows the exact same pattern used for `m0001_initial` (discovered from sibling analysis).
