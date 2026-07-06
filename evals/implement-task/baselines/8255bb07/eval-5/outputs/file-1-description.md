# File 1: `migration/src/lib.rs` (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so the migration runner includes it when applying migrations.

## Current State (expected)

The file currently declares one migration module and returns it in a list:

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

### Change 1: Add module declaration

**Location**: After `mod m0001_initial;`

**Add**:
```rust
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations list

**Location**: Inside the `migrations()` function, after `Box::new(m0001_initial::Migration),` in the `vec![]`

**Add**:
```rust
Box::new(m0002_drop_advisory_status::Migration),
```

## Result (after changes)

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;

use sea_orm_migration::prelude::*;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m0001_initial::Migration),
            Box::new(m0002_drop_advisory_status::Migration),
        ]
    }
}
```

## Rationale

- The new migration must be registered after `m0001_initial` to ensure sequential execution (migrations run in order)
- The module declaration follows the same pattern as the existing `m0001_initial` declaration
- The `Box::new()` wrapping matches the existing pattern for trait object creation
