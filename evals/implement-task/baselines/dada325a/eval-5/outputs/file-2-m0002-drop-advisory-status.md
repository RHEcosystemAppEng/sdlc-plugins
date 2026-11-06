# File 2 — `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

## Purpose
A SeaORM migration that drops the deprecated `status` column from the `advisory` table, with a reversible `down` that adds it back as a nullable string.

## Pattern source
`migration/src/m0001_initial/mod.rs` provides the `DeriveMigrationName` + `#[async_trait::async_trait] impl MigrationTrait for Migration`, the `use sea_orm_migration::prelude::*;` import, and the module-local `#[derive(DeriveIden)]` enums.

## Full file content

```rust
//! Drops the deprecated `status` column from the `advisory` table.
//!
//! The column was superseded by the `severity` enum field and is no longer
//! read or written by any entity or service code.

use sea_orm_migration::prelude::*;

/// Migration that removes `advisory.status` (rollback re-adds it as a nullable string).
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

    /// Re-adds the `status` column as a nullable string so the migration can be rolled back.
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

/// Identifiers for the `advisory` table columns touched by this migration.
///
/// Declared locally (rather than imported from `m0001_initial`) so this
/// migration stays a stable, self-contained snapshot of the schema change.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}

#[cfg(test)]
mod tests {
    use super::*;
    use sea_orm::{ConnectionTrait, DatabaseBackend, Statement};
    use sea_orm_migration::MigratorTrait;

    /// Returns `(data_type, is_nullable)` for `advisory.status`, or `None` if the column is absent.
    async fn status_column(db: &impl ConnectionTrait) -> Option<(String, String)> {
        let row = db
            .query_one(Statement::from_string(
                DatabaseBackend::Postgres,
                "SELECT data_type, is_nullable FROM information_schema.columns \
                 WHERE table_name = 'advisory' AND column_name = 'status'",
            ))
            .await
            .expect("information_schema query should succeed")?;
        Some((
            row.try_get("", "data_type").expect("data_type"),
            row.try_get("", "is_nullable").expect("is_nullable"),
        ))
    }

    /// Verifies that applying all migrations removes the `status` column from `advisory`.
    #[tokio::test]
    async fn up_drops_advisory_status_column() {
        // Given a fresh test database (same bootstrap helper used by the repo's DB tests)
        let db = crate::test_support::fresh_db().await;

        // When all migrations, including m0002, are applied
        crate::Migrator::up(&db, None).await.expect("migrations should apply");

        // Then the status column no longer exists
        assert_eq!(status_column(&db).await, None);
    }

    /// Verifies that rolling back m0002 re-adds `status` as a nullable varchar column.
    #[tokio::test]
    async fn down_readds_nullable_status_column() {
        // Given a database with all migrations applied
        let db = crate::test_support::fresh_db().await;
        crate::Migrator::up(&db, None).await.expect("migrations should apply");

        // When the most recent migration (m0002) is rolled back
        crate::Migrator::down(&db, Some(1)).await.expect("rollback should succeed");

        // Then the status column is back as a nullable character varying
        assert_eq!(
            status_column(&db).await,
            Some(("character varying".to_string(), "YES".to_string()))
        );
    }
}
```

## Notes
- `crate::test_support::fresh_db()` is a placeholder for whatever test DB bootstrap the repo already uses (found during Step 4 sibling analysis, e.g. the helper used by `tests/` or an existing `migration` test). The real helper is reused, not a new one written. If the migration crate has no in-crate DB helper and one would have to be added outside this file, that would be flagged as out of scope.
- The assertions check concrete values (column absence; exact `data_type` and `is_nullable`). They do not check row counts.
- Test requirement (c), that existing advisory queries still work, is covered by re-running the existing `tests/api/advisory.rs` suite against the migrated schema. That file is out of scope for edits.
- Before this file is created, Step 4 confirms that `entity/src/advisory.rs` has no `status` field and that no code under `modules/` references it. If either check fails, the task stops.
