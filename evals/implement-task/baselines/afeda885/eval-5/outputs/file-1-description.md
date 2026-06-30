# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This is a new file. It implements the `MigrationTrait` from SeaORM, following the exact pattern established in `migration/src/m0001_initial/mod.rs`.

### Structure

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

/// Enum representing the advisory table and its columns for use in migration statements.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **Pattern conformance**: Follows the exact same `MigrationTrait` implementation pattern as `m0001_initial/mod.rs`
2. **Rollback safety**: The `down` method re-adds `status` as a nullable string (`string().null()`), so rollback does not break existing rows that lack a value
3. **Local `Iden` enum**: Defines a local `Advisory` enum with `Table` and `Status` variants for use in the migration, rather than importing from the entity crate (which no longer has the `Status` variant since it was removed)
4. **Documentation**: All public items have doc comments per the skill's code quality practices
