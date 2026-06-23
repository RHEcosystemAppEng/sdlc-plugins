# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This follows the existing migration pattern established by `m0001_initial/mod.rs`.

## Detailed Implementation

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code. Removing it
/// reduces confusion and prevents accidental usage.
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

    /// Re-add the `status` column as a nullable string for rollback support.
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

/// Enum identifying the `advisory` table and its columns for SeaORM schema operations.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Design Decisions

1. **`DeriveMigrationName` macro**: Used to auto-derive the migration name from the module path, consistent with m0001_initial.

2. **`Advisory` Iden enum**: Defines only the `Table` and `Status` variants needed for this migration. This is a local enum scoped to the migration module -- it does not conflict with the entity definition in `entity/src/advisory.rs`.

3. **`up` method**: Uses `Table::alter()` with `drop_column()` to remove the column. This matches the SeaORM `TableAlterStatement` approach referenced in the task's Implementation Notes.

4. **`down` method**: Re-adds the column as `string().null()` (nullable string). This ensures rollback doesn't fail on existing rows that won't have a value for the restored column. This matches the Implementation Notes specification.

5. **Doc comments**: Added to the struct, `up`, `down`, and the `Iden` enum per the skill's code quality practices requirement.

## Conventions Followed

- Same module structure as `m0001_initial/mod.rs` (trait implementation, Iden enum)
- Same `async_trait` pattern for `MigrationTrait` implementation
- Same SeaORM schema builder API usage
- Migration directory naming follows `m<NNNN>_<snake_case_description>` pattern
