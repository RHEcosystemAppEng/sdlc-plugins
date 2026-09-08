# File 2: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

Database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer referenced by any service or entity code.

## File Content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field and is no longer
/// read or written by any service code. Removing it prevents accidental usage and
/// reduces schema confusion.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

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
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}

/// Enum identifying the `advisory` table and its columns for type-safe schema operations.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

### Following sibling pattern (m0001_initial/mod.rs)
- Same struct name `Migration` implementing `MigrationTrait`
- Same `MigrationName` implementation returning the module directory name
- Same async `up`/`down` pattern with `SchemaManager`

### Column definition in `down` method
- Re-adds `status` as `.string().null()` -- nullable to avoid breaking existing rows that would have no value for this column after rollback
- This matches the Implementation Notes specification exactly

### Local `Advisory` Iden enum
- Defines a local `Advisory` enum with `Iden` derive for type-safe table/column references
- Only includes `Table` and `Status` variants since those are the only identifiers needed for this migration
- This is a common SeaORM migration pattern -- migrations define their own Iden enums rather than importing from entity crate, because entity definitions may change over time while migrations must remain stable

## Pre-Implementation Verification Required

Before creating this file, verify:
1. `entity/src/advisory.rs` does NOT reference a `status` column (confirming it is truly deprecated)
2. Search service code (modules/fundamental/src/advisory/, modules/ingestor/src/graph/advisory/) for any `status` column references
3. Read `migration/src/m0001_initial/mod.rs` to confirm the exact struct/trait pattern used

## Acceptance Criteria Coverage

| Criterion | How Satisfied |
|-----------|--------------|
| Migration drops the `status` column | `up()` uses `drop_column(Advisory::Status)` |
| Down method re-adds as nullable string | `down()` uses `ColumnDef::new(Advisory::Status).string().null()` |
| Migration registered in lib.rs | Covered in file-1-description.md |
| No service/entity code references status | Pre-implementation verification step |
