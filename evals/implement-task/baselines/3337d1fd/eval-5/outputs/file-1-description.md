# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner includes it when running migrations.

## Current State (Expected)

The file currently:
- Declares `mod m0001_initial;`
- Implements a struct (e.g., `Migrator`) that provides a `migrations()` function
- The `migrations()` function returns a `Vec<Box<dyn MigrationTrait>>` containing `Box::new(m0001_initial::Migration)`

## Changes

### 1. Add module declaration

Add a new module declaration after the existing one:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- ADD THIS LINE
```

### 2. Register migration in migrations() function

Add the new migration to the `vec![]` inside the `migrations()` function, after the existing `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- ADD THIS LINE
    ]
}
```

## Conventions Followed

- Follows the same registration pattern as `m0001_initial`
- Migration ordering is chronological (m0001 before m0002)
- Module naming matches the directory name exactly
