# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

Implement a SeaORM migration that drops the deprecated `status` column from the `advisory` table. The `down` method re-adds the column as a nullable string to support rollback.

## File Location

`migration/src/m0002_drop_advisory_status/mod.rs`

This follows the existing directory convention where each migration lives in its own directory (e.g., `m0001_initial/mod.rs`).

## Full Implementation

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code.

use sea_orm_migration::prelude::*;

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

/// Identifiers for the `advisory` table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`DeriveMigrationName` macro**: Generates a unique migration name from the module path, consistent with `m0001_initial`
2. **`Advisory` enum with `DeriveIden`**: Defines table/column identifiers locally within this migration module, following SeaORM conventions. This avoids coupling to the entity definitions (which already removed `status`)
3. **`up` method**: Uses `TableAlterStatement` with `drop_column` as specified in the Implementation Notes
4. **`down` method**: Re-adds the column as `string().null()` -- nullable to avoid breaking existing rows that would have no value for this column after rollback
5. **Module-level doc comment**: Documents why this migration exists, following code quality practices

## Conventions Applied

- Follow the same `MigrationTrait` implementation pattern as `m0001_initial/mod.rs`
- Use `async_trait` for the trait implementation
- Define table/column identifiers using `DeriveIden` enum local to the migration
- Use `to_owned()` on the builder chain before passing to `manager`
- Include doc comments on both the module and the public methods

## Acceptance Criteria Coverage

- [x] Migration drops the `status` column from the `advisory` table (via `up` method)
- [x] Migration `down` method re-adds the column as nullable string for rollback
- [x] Migration is registered in `migration/src/lib.rs` (covered by file-1-description.md)
- [x] No service or entity code references the `status` column (verified pre-implementation)

## Test Requirements Coverage

- Test that the migration runs successfully against a test database: run `cargo test` which exercises migrations against the test PostgreSQL instance
- Test that the rollback (down) re-adds the column: verify by running up then down migration in the test suite
- Verify that existing advisory queries still work after the column is dropped: the advisory endpoint integration tests in `tests/api/advisory.rs` should continue to pass since the entity no longer references `status`
