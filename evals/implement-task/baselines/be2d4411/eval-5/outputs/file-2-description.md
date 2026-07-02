# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

Create a new SeaORM migration that drops the deprecated `status` column from the `advisory` table.

## Pattern Reference

This file follows the pattern established by `migration/src/m0001_initial/mod.rs`, implementing the `MigrationTrait` with `up` and `down` methods.

## Inspection Required Before Creating

- Read `migration/src/m0001_initial/mod.rs` to understand the exact migration pattern (imports, struct definition, trait implementation, naming conventions)
- Read `entity/src/advisory.rs` to verify that the `status` column is NOT referenced in the entity definition (confirming it is safe to drop)
- Grep across `modules/fundamental/src/advisory/` and other service code for any remaining references to `status` on the advisory entity

## File Contents

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
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

/// Identifiers for the advisory table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Design Decisions

1. **`up` method**: Uses `TableAlterStatement` to drop the `status` column, as specified in the implementation notes
2. **`down` method**: Re-adds the column as `string().null()` (nullable string) to allow rollback without breaking existing rows that would lack a value
3. **`Advisory` enum**: Defines `DeriveIden` identifiers for the table and column names used in the alter statements, following SeaORM conventions
4. **Migration name**: Derived automatically by `DeriveMigrationName` from the module path (`m0002_drop_advisory_status`)
