# File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the existing migration pattern established by `m0001_initial/mod.rs`.

## Sibling Analysis

Pattern derived from `migration/src/m0001_initial/mod.rs`:
- Implements `MigrationTrait` with `up` and `down` async methods
- Uses SeaORM's `SchemaManager` for DDL operations
- References entity enums (e.g., `Advisory::Table`, `Advisory::Status`) for table/column identifiers
- Returns `Result<(), DbErr>`

## Detailed Contents

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drop the deprecated `status` column from the `advisory` table.
    /// This column was replaced by the `severity` enum field and is no
    /// longer read or written by any service code.
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

    /// Re-add the `status` column as a nullable string to allow rollback.
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

#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`DeriveMigrationName`**: Used to auto-generate the migration name from the module path, consistent with SeaORM conventions.
2. **Local `Advisory` Iden enum**: The migration defines its own `Advisory` Iden enum with only the identifiers it needs (`Table` and `Status`), rather than importing from the entity crate. This is standard SeaORM migration practice -- migrations must be self-contained so they remain valid even if the entity definitions change in the future.
3. **Nullable string on rollback**: The `down` method re-adds `status` as `.string().null()` so that rollback does not break existing rows that have no value for this column.
4. **Doc comments on methods**: Each method has a doc comment explaining what it does and why, following best practices for migration clarity.
