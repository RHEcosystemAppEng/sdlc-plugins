# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Detailed Changes

Create a new file implementing the `MigrationTrait` from SeaORM, following the pattern established in `migration/src/m0001_initial/mod.rs`.

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer referenced by any entity or service code.
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

    /// Re-adds the `status` column as a nullable string to allow rollback.
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

/// Iden enum for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Implementation Details

1. **`up` method:** Uses `TableAlterStatement` via `Table::alter()` to drop the `status` column, exactly as specified in the Implementation Notes
2. **`down` method:** Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback -- the column is nullable so existing rows are not affected on rollback
3. **`Iden` enum:** Defines the `Advisory` enum with `Table` and `Status` variants for type-safe table/column references in SeaORM
4. **Documentation:** Every public symbol has a doc comment explaining its purpose, following the SKILL.md requirement for documentation on new symbols
5. **Pattern conformance:** Follows the same structure as `m0001_initial/mod.rs` -- implements `MigrationName` and `MigrationTrait`, uses `async_trait`, and returns `Result<(), DbErr>`
