# File 1: `migration/src/lib.rs` (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner includes it when running migrations.

## Current State (Expected)

The file currently declares one migration module and registers it in a `migrations()` function:

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

Add the new module declaration after the existing `m0001_initial` declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### 2. Register migration in the migrations vector

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

- The migration must be registered for the migration runner to discover and execute it.
- Ordering matters: `m0002` must come after `m0001` since migrations run sequentially.
- The pattern follows the exact same registration used for `m0001_initial`.

## Verification

- After modification, `cargo build` should compile without errors.
- The migration runner should list `m0002_drop_advisory_status` when showing pending migrations.
