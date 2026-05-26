# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list
so that the SeaORM migration runner discovers and executes it.

## Inspection basis

Before modifying this file, the current content of `migration/src/lib.rs` was read.
The file follows this structure:

```rust
// (existing content — representative)
pub use sea_orm_migration::prelude::*;

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

## Changes to make

### 1. Add module declaration

After the existing `mod m0001_initial;` line, add:

```rust
mod m0002_drop_advisory_status;
```

### 2. Append migration to the vec

Inside the `migrations()` function's `vec![]`, append a new entry after
`Box::new(m0001_initial::Migration)`:

```rust
Box::new(m0002_drop_advisory_status::Migration),
```

## Resulting file content (after modification)

```rust
pub use sea_orm_migration::prelude::*;

mod m0001_initial;
mod m0002_drop_advisory_status;

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

## Key design decisions

1. **Order preserved**: `m0001_initial` remains first. The new migration is appended at
   the end, which is required — SeaORM runs migrations in the order they appear in the
   `vec![]`. Appending ensures `m0002` only runs after `m0001` has completed.

2. **Module declaration placement**: the `mod m0002_drop_advisory_status;` declaration
   is placed directly after `mod m0001_initial;` to keep module declarations grouped
   together at the top of the file, consistent with Rust conventions and the existing
   file structure.

3. **Minimal change**: only the module declaration and one `vec![]` entry are added.
   No other changes are made to `lib.rs`. This satisfies the scope containment
   requirement in Step 9.
