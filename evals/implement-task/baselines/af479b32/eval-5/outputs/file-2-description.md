# File 2: `migration/src/m0002_drop_advisory_status/mod.rs` (Create)

## Purpose

Implement a SeaORM migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Full File Content

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a prior migration
//! and is no longer referenced by any entity or service code. Removing it reduces
//! confusion and prevents accidental usage.

use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the `status` column from the `advisory` table.
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .drop_column(Advisory::Status)
                    .to_owned(),
            )
            .await
    }

    /// Re-adds the `status` column as a nullable string for rollback support.
    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}

/// Identifiers for the `advisory` table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

### MigrationTrait Implementation
- Follows the exact pattern from `m0001_initial/mod.rs` -- implements `MigrationTrait` with async `up()` and `down()` methods.
- Uses `#[derive(DeriveMigrationName)]` to auto-generate the migration name from the module path.
- Uses `#[async_trait::async_trait]` for async trait methods, matching the sibling migration.

### Up Method (Forward Migration)
- Uses `Table::alter()` to modify the existing `advisory` table.
- Calls `drop_column(Advisory::Status)` to remove the deprecated column.
- Ends with `.to_owned()` to produce an owned statement, per SeaORM convention.
- The SQL generated will be: `ALTER TABLE advisory DROP COLUMN status`

### Down Method (Rollback)
- Re-adds the `status` column using `ColumnDef::new(Advisory::Status).string().null()`.
- The column is nullable (`.null()`) to avoid breaking existing rows that have no status value.
- The column type is string (`.string()`) matching its original definition.
- The SQL generated will be: `ALTER TABLE advisory ADD COLUMN status VARCHAR NULL`

### Local Iden Enum
- Defines a local `Advisory` enum with `#[derive(Iden)]` containing only the identifiers needed for this migration (`Table` and `Status`).
- This is self-contained -- the migration does not depend on the entity module's `Advisory` enum, which may evolve independently.
- This is a common SeaORM migration pattern: migrations define their own identifiers to remain stable even if entity definitions change in the future.

### Documentation
- Module-level doc comment explains the purpose and rationale for the migration.
- Doc comments on `up()` and `down()` describe what each method does.
- The `Advisory` enum has a doc comment explaining its role.

## Verification

- `cargo build` in the `migration` crate should compile successfully.
- `cargo test` should pass, including any migration integration tests.
- Running the migration against a test database should:
  - Drop the `status` column from the `advisory` table (up)
  - Re-add the `status` column as nullable string (down/rollback)
- Existing advisory queries should continue to work since no code references the `status` column.
