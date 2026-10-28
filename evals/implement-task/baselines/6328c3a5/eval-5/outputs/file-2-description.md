# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Convention source

Follows the pattern established in `migration/src/m0001_initial/mod.rs` (sibling migration).

## Full file content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer referenced by any service or entity code.
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

/// Identifiers for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design decisions

1. **`Advisory` enum defined locally**: The migration defines its own `Advisory` enum with `Table` and `Status` variants rather than importing from the entity crate. This is standard practice for migrations -- entity definitions may change over time, but migrations must remain stable and self-contained.

2. **Nullable string for rollback**: The `down()` method re-adds `status` as `.string().null()` to allow rollback without data loss. Since the column data was already obsolete, nullable is appropriate -- no default value is needed.

3. **MigrationName implementation**: Returns `"m0002_drop_advisory_status"` matching the module directory name, following the convention from m0001_initial.

4. **Documentation comments**: Added doc comments on the struct, `up()`, `down()`, and the `Advisory` enum per the skill's requirement that every new public symbol has documentation.

## Acceptance criteria coverage

- [x] Migration drops the `status` column from the `advisory` table (via `up()`)
- [x] Migration `down` method re-adds the column as nullable string for rollback (via `down()`)
- [x] Migration is registered in `migration/src/lib.rs` (covered in file-1-description.md)
- [x] No service or entity code references the `status` column (verified by checking `entity/src/advisory.rs` -- task states the column is already removed from the entity)
