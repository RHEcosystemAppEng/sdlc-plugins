# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration runner so it is discovered and executed during database migrations.

## Current State (Expected)

The file currently declares the `m0001_initial` module and returns it in the `migrations()` function. Based on the sibling pattern, the structure looks like:

```rust
mod m0001_initial;

use sea_orm_migration::prelude::*;

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

Add a new module declaration for `m0002_drop_advisory_status` after the existing `m0001_initial` declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### 2. Register migration in the vec

Add the new migration to the `vec![]` in the `migrations()` function, after `m0001_initial`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Rationale

- The module declaration makes the new migration module visible to the `lib.rs` scope
- Adding it to the `migrations()` vec ensures SeaORM's migration runner discovers and executes it in order
- The migration is placed after `m0001_initial` to maintain chronological ordering, matching the naming convention (m0001, m0002, ...)
