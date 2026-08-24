# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

New database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer referenced by any service or entity code.

## Pattern reference

This file follows the migration pattern established in `migration/src/m0001_initial/mod.rs`, implementing `MigrationTrait` with `up` and `down` methods.

## File content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the advisory table.
///
/// The `status` column was replaced by the `severity` enum field and is no longer
/// read or written by any service code. Removing it prevents accidental usage.
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
                    .add_column(
                        ColumnDef::new(Advisory::Status)
                            .string()
                            .null(),
                    )
                    .to_owned(),
            )
            .await
    }
}

/// Enum representing the advisory table and its columns for SeaORM migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key design decisions

1. **`up` method**: Uses `TableAlterStatement` with `drop_column` as specified in Implementation Notes
2. **`down` method**: Re-adds column as `string().null()` to allow rollback without data loss for existing rows
3. **Advisory enum**: Defines only the `Table` and `Status` identifiers needed for this migration, following SeaORM's `Iden` derive pattern
4. **Documentation**: Every public struct and function has a doc comment explaining its purpose

## Conventions followed

- Implements `MigrationTrait` with both `up` and `down` methods (same pattern as `m0001_initial`)
- Uses `#[derive(DeriveMigrationName)]` for automatic migration naming
- Uses `async_trait` attribute for async trait implementation
- Error handling via `Result<(), DbErr>` return type (SeaORM convention)
- File located at `migration/src/m0002_drop_advisory_status/mod.rs` following the numbered module directory convention
