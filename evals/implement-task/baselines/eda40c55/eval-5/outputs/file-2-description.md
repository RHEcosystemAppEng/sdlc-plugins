# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

New migration that drops the deprecated `status` column from the `advisory` table, with a `down` method that re-adds it as a nullable string for rollback support.

## Pattern Reference

This file follows the pattern established in `migration/src/m0001_initial/mod.rs`, implementing the `MigrationTrait` with `up` and `down` methods.

## Full File Content

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

#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`up` method**: Uses `TableAlterStatement` with `drop_column` as specified in the Implementation Notes. This is the SeaORM idiomatic way to alter tables.

2. **`down` method**: Re-adds the `status` column as a nullable string (`string().null()`). Making it nullable ensures rollback does not fail on existing rows that lack a value for this column. This matches the Implementation Notes specification.

3. **`Iden` enum**: A local `Advisory` enum implementing the `Iden` trait provides type-safe table and column identifiers for the migration. This follows SeaORM migration conventions where each migration defines its own identifiers rather than importing from the entity crate (migrations should be self-contained and not depend on entity definitions that may change over time).

4. **`MigrationName`**: Returns `"m0002_drop_advisory_status"` matching the module directory name, following the convention established by `m0001_initial`.

5. **Documentation**: A doc comment on the `Migration` struct explains why the migration exists, per the skill's code quality practices requirement.
