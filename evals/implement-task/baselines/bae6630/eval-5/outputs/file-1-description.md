# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migrator discovers and runs it.

## Pre-Modification Inspection

Before modifying this file, read it to understand:
- How the existing `m0001_initial` module is declared
- The structure of the `migrations()` function and its return type
- The ordering convention for migration entries in the `vec![]`

## Changes

### 1. Add module declaration

Add a new `mod` statement for the migration module, following the existing pattern:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- new
```

### 2. Register in migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function. It must be appended after `m0001_initial` to maintain chronological migration order:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- new
    ]
}
```

## Conventions Applied

- Follow the same `mod` declaration style as `m0001_initial`
- Follow the same `Box::new(module::Migration)` registration pattern
- Maintain chronological ordering of migrations in the vec
