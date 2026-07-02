# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

New migration that drops the deprecated `status` column from the `advisory` table and provides a rollback path.

## Full File Content

The file follows the pattern established in `migration/src/m0001_initial/mod.rs`:

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer referenced by any entity or service code.
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

/// Enum representing the `advisory` table and its columns for SeaORM migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`MigrationName::name()`** returns `"m0002_drop_advisory_status"` following the naming convention of existing migrations (module directory name).

2. **`up` method** uses `Table::alter().drop_column()` as specified in the Implementation Notes. This is a destructive operation that removes the column and its data.

3. **`down` method** re-adds the column as `string().null()` per the Implementation Notes. The column is nullable so that existing rows (which will have no value after rollback) are valid without a default. This matches the rollback-safety pattern.

4. **`Advisory` Iden enum** is defined locally within the migration module (not imported from `entity/src/advisory.rs`) because the entity definition no longer includes `Status`. Each migration must be self-contained and not depend on the current state of entity definitions, which may change over time.

## Convention Conformance

- Follows the `MigrationTrait` implementation pattern from `m0001_initial/mod.rs`
- Uses `async_trait` macro consistently with existing migrations
- Uses the `Iden` derive for table/column identifiers as established in the codebase
- Documentation comments on all public items and methods
