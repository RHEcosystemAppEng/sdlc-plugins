# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

Create this file following the pattern established in `migration/src/m0001_initial/mod.rs`. The file implements the `MigrationTrait` trait from SeaORM with `up` and `down` methods.

### File Content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
/// Removing it reduces confusion and prevents accidental usage.
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

#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **Follows m0001_initial pattern**: Uses the same `MigrationTrait` implementation pattern with `up` and `down` methods, matching the existing migration structure.
2. **Local Iden enum**: Defines a local `Advisory` enum with `Table` and `Status` variants for use with SeaORM's `TableAlterStatement`, keeping the migration self-contained rather than importing from the entity crate (which may have already removed the `Status` variant).
3. **Nullable rollback**: The `down` method re-adds `status` as `.string().null()` so that rollback does not require backfilling data -- existing rows will have NULL for the restored column.
4. **Documentation**: Doc comments on the struct and both methods explain the purpose and rationale.
