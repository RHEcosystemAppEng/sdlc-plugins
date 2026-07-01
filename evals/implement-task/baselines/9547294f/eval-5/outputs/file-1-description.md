# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

Create a new file implementing the `MigrationTrait` for SeaORM, following the pattern established by `m0001_initial/mod.rs`.

### Full file content

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code.

use sea_orm_migration::prelude::*;

/// Migration that removes the deprecated `status` column from the advisory table.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drop the `status` column from the `advisory` table.
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

    /// Re-add the `status` column as a nullable string for rollback.
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

/// Iden enum for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Design Decisions

1. **`DeriveMigrationName`**: Uses the derive macro (consistent with SeaORM conventions) to auto-generate the migration name from the module path.
2. **Local `Iden` enum**: Defines a local `Advisory` enum with only `Table` and `Status` variants rather than importing from the entity crate. This is a migration best practice — migrations should be self-contained and not depend on entity definitions that may change over time.
3. **Nullable string for rollback**: The `down` method re-adds the column as `.string().null()` — nullable because existing rows won't have data for this column after rollback.
4. **Doc comments**: Every public symbol has a `///` documentation comment per the project's Rust conventions and the skill's code quality requirements.
