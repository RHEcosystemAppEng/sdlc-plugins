# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

New migration that drops the deprecated `status` column from the `advisory` table. This column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## File structure

The file follows the pattern established in `migration/src/m0001_initial/mod.rs`:

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field and is no longer
/// referenced by any entity or service code.
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

/// Enum identifiers for the advisory table and its columns, used by SeaORM's
/// schema alteration API.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key design decisions

### up method
- Uses `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)` as specified in Implementation Notes
- Follows the exact SeaORM API pattern from the task description

### down method
- Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` as specified in Implementation Notes
- Column is nullable to allow rollback without breaking existing rows (rows created after the `up` migration ran will have no status value)

### Iden enum
- Defines `Advisory::Table` and `Advisory::Status` identifiers for use with SeaORM's type-safe table alteration API
- This is the standard SeaORM pattern for referencing tables and columns in migrations

## Conventions followed

- File placed in `migration/src/m0002_drop_advisory_status/mod.rs` following the `m<NNNN>_<description>/mod.rs` directory structure from `m0001_initial`
- Implements `MigrationName` and `MigrationTrait` traits (same as `m0001_initial`)
- Uses `async_trait` attribute macro for async trait methods
- Returns `Result<(), DbErr>` from both `up` and `down` methods
- Documentation comments on the struct and both methods

## Pre-implementation verification

Before creating this file, the entity at `entity/src/advisory.rs` was inspected to confirm that:
- The `status` column is NOT referenced in the entity definition
- Only the `severity` field (its replacement) is present
- No service code in `modules/fundamental/src/advisory/` references the `status` column
