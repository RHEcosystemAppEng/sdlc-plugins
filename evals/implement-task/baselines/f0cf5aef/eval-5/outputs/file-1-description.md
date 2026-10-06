# File 1: CREATE `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: Create new file

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

Create the file following the pattern established by the sibling migration `migration/src/m0001_initial/mod.rs`. The file implements `MigrationTrait` from SeaORM with `up` and `down` methods.

### Expected content

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
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
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}

/// Identifiers for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Conventions followed

- Follows the `MigrationTrait` implementation pattern from `m0001_initial/mod.rs`
- Uses `#[derive(DeriveMigrationName)]` for automatic migration naming
- Uses `async_trait` for async trait implementation
- Uses SeaORM's `Table::alter()` and `TableAlterStatement` API
- Declares a local `Advisory` Iden enum for table/column identifiers (standard SeaORM pattern for migrations -- migrations define their own Iden enums rather than importing from the entity crate, so they remain self-contained and do not break if entity definitions change later)
- Documentation comments on the struct and both methods
- The `down` method re-adds the column as `string().null()` to allow rollback without breaking existing rows

### Pre-implementation verification

Before creating this file, verify:
1. `entity/src/advisory.rs` does NOT reference a `status` column (confirming it was already removed from the entity)
2. No service code in `modules/` references `Advisory::Status` or a `status` field on advisories
3. The `m0001_initial/mod.rs` pattern matches what is described above (imports, derive macros, trait implementation structure)
