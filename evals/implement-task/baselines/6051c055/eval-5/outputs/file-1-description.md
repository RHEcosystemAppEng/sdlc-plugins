# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration file that drops the deprecated `status` column from the `advisory` table.

## Pattern Reference

This file follows the pattern established in `migration/src/m0001_initial/mod.rs`, which
implements `MigrationTrait` with `up()` and `down()` methods using SeaORM's schema API.

## Detailed Changes

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

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

    /// Re-adds the `status` column as a nullable string for rollback.
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

/// Enum identifying the advisory table and its columns for SeaORM's Iden trait.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Implementation Details

- **`up()` method:** Uses `Table::alter()` with `.drop_column(Advisory::Status)` to remove
  the column via SeaORM's `TableAlterStatement` API.
- **`down()` method:** Uses `Table::alter()` with `.add_column()` to re-add the column as
  `ColumnDef::new(Advisory::Status).string().null()` -- a nullable string, as specified in
  the Implementation Notes. This ensures the rollback does not impose a NOT NULL constraint
  on existing rows.
- **`Advisory` enum:** A local Iden enum that maps `Table` to the `advisory` table name and
  `Status` to the `status` column name. This follows SeaORM's pattern for type-safe table
  and column references in migrations.
- **Documentation:** Every public symbol has a doc comment explaining its purpose, per the
  skill's code quality practices.
