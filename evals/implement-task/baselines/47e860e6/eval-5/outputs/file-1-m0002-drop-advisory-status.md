# File 1 (CREATE): `migration/src/m0002_drop_advisory_status/mod.rs`

Listed in the task's **Files to Create**. It follows the pattern of `migration/src/m0001_initial/mod.rs`.

```rust
//! Migration that drops the deprecated `status` column from the `advisory` table.
//!
//! The column was superseded by the `severity` enum field and is no longer read
//! or written by any service or entity code.

use sea_orm_migration::prelude::*;

/// Drops `advisory.status`; rollback re-adds it as a nullable string.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
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
/// Declared locally (not shared with `m0001_initial`) so this migration remains an
/// immutable snapshot of the schema at the time it was written.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::Migrator;
    use sea_orm::{ConnectionTrait, DatabaseBackend, FromQueryResult, Statement};
    use sea_orm_migration::MigratorTrait;

    /// Row shape for an `information_schema.columns` lookup.
    #[derive(Debug, PartialEq, FromQueryResult)]
    struct ColumnInfo {
        data_type: String,
        is_nullable: String,
    }

    /// Looks up `advisory.status` in `information_schema`; `None` if absent.
    async fn advisory_status_column(db: &impl ConnectionTrait) -> Option<ColumnInfo> {
        ColumnInfo::find_by_statement(Statement::from_string(
            DatabaseBackend::Postgres,
            "SELECT data_type, is_nullable FROM information_schema.columns \
             WHERE table_name = 'advisory' AND column_name = 'status'",
        ))
        .one(db)
        .await
        .expect("information_schema query")
    }

    /// Verifies that applying all migrations removes the `status` column from `advisory`.
    #[tokio::test]
    async fn test_up_drops_advisory_status_column() {
        // Given a fresh test database
        let db = test_db().await;

        // When all migrations are applied
        Migrator::up(&db, None).await.expect("migrate up");

        // Then advisory.status no longer exists
        assert_eq!(advisory_status_column(&db).await, None);
    }

    /// Verifies that rolling back m0002 re-adds `status` as a nullable varchar column.
    #[tokio::test]
    async fn test_down_readds_advisory_status_column() {
        // Given a database with all migrations applied
        let db = test_db().await;
        Migrator::up(&db, None).await.expect("migrate up");

        // When the latest migration (m0002) is rolled back
        Migrator::down(&db, Some(1)).await.expect("migrate down");

        // Then advisory.status exists as a nullable string
        assert_eq!(
            advisory_status_column(&db).await,
            Some(ColumnInfo {
                data_type: "character varying".into(),
                is_nullable: "YES".into(),
            })
        );
    }
}
```

`test_db()` is a placeholder for the repo's existing PostgreSQL test-database bootstrap helper, which `tests/` already uses. I would find it in Step 4 with `search_for_pattern("async fn .*db|TestContext|test_db")` and reuse it rather than write a new one.

Notes:
- `up` and `down` use exactly the statements from the Implementation Notes.
- Each test has a `///` doc comment and `// Given / // When / // Then` sections.
- The rollback test asserts on column values (type and nullability) rather than on a count.
- Test requirement (c), that existing advisory queries still work, is covered by running the existing `tests/api/advisory.rs` suite after the migration. A new test in that file would be out of scope and needs user approval first.
- Dev-dependencies (`tokio`, `sea-orm` with the postgres runtime) may be needed in `migration/Cargo.toml`. That file is out of scope, so if the dependencies are missing it would be flagged in Step 9 rather than edited.
