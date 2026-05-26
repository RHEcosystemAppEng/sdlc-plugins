# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

This is the new migration module that drops the deprecated `status` column from the
`advisory` table. It follows the pattern established by `migration/src/m0001_initial/mod.rs`.

## Inspection basis

Before writing this file, `migration/src/m0001_initial/mod.rs` was read to confirm:
- The import block uses `sea_orm_migration::prelude::*`
- Migrations declare `pub struct Migration` as a unit struct
- `MigrationName` is implemented by returning a static string matching the module directory name
- `MigrationTrait` is implemented with two async methods: `up` and `down`
- Schema operations use `manager.alter_table(...)` / `manager.create_table(...)` chained with `.to_owned().await`

`entity/src/advisory.rs` was also inspected to confirm that:
- The `Advisory::Status` column variant does **not** appear in the current entity definition
- The entity uses `Advisory::Severity` (an enum), which replaced `status`
- There are no remaining references to `Advisory::Status` in entity code

## Full file content

```rust
//! Migration m0002_drop_advisory_status
//!
//! Drops the deprecated `status` column from the `advisory` table.
//! The column was superseded by the `severity` enum field and is no
//! longer read or written by any service or entity code.

use sea_orm_migration::prelude::*;

/// Migration that removes the obsolete `status` column from the `advisory` table.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

/// Column identifier enum for the `advisory` table.
///
/// Used locally within this migration to reference the table and column
/// being altered without depending on the entity crate's column enum,
/// which no longer includes `Status`.
#[derive(Iden)]
enum Advisory {
    Table,
    /// The deprecated status column being dropped in `up` and re-added in `down`.
    Status,
}

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the `status` column from the `advisory` table.
    ///
    /// After this migration, the column is permanently absent from the schema.
    /// Use `down` to reverse.
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

    /// Re-adds the `status` column to the `advisory` table as a nullable string.
    ///
    /// Restores the column to allow rollback; the column will be empty for rows
    /// created after the original migration.
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
```

## Key design decisions

1. **Local `Advisory` enum**: The entity crate's `Advisory` column enum no longer contains
   `Status` (confirmed during Step 4 inspection). A local `#[derive(Iden)]` enum is used
   inside the migration module to reference the table and column without coupling the
   migration to a potentially-changing entity definition.

2. **`up` uses `drop_column`**: Directly maps to the SeaORM `TableAlterStatement` API
   described in the Implementation Notes. The column is dropped unconditionally.

3. **`down` uses `add_column` with `.string().null()`**: Re-adds the column as a nullable
   string, matching what the Implementation Notes specify and allowing rollback without
   data loss constraints. Rows that existed after the original migration will have `NULL`
   for this column upon rollback.

4. **Doc comments on all public symbols**: `Migration`, `Advisory`, `up`, and `down` all
   carry `///` doc comments per the code quality practices in the skill definition.

5. **`async_trait`**: Required because `MigrationTrait` uses async methods; the attribute
   macro `#[async_trait::async_trait]` is applied consistent with the sibling migration.
