# File 1 — `migration/src/lib.rs` (Modify)

## Purpose
Register the new `m0002_drop_advisory_status` migration so `Migrator` runs it after `m0001_initial`.

## Pre-check
`mcp__serena_backend__find_symbol("Migrator", relative_path="migration/src/lib.rs", include_body=true)` to confirm
the existing shape (expected standard SeaORM layout shown below).

## Expected current content (pattern)

```rust
pub use sea_orm_migration::prelude::*;

mod m0001_initial;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![Box::new(m0001_initial::Migration)]
    }
}
```

## Changes

1. Add the module declaration directly after `mod m0001_initial;` (keep numeric order):

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

2. Append the migration to the `vec![]` in `migrations()`, after `m0001_initial` (order matters — migrations run sequentially):

```rust
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m0001_initial::Migration),
            Box::new(m0002_drop_advisory_status::Migration),
        ]
    }
```

No other changes to this file. Implemented via `mcp__serena_backend__replace_symbol_body` on `migrations` (or Edit as fallback)
and `insert_after_symbol` / Edit for the `mod` line.
