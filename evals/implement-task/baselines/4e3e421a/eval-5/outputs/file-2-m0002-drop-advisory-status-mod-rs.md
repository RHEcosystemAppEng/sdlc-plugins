# File 2 — `migration/src/m0002_drop_advisory_status/mod.rs` (Create)

## Purpose
Drop the deprecated `status` column from the `advisory` table (superseded by the `severity` enum); `down` re-adds it
as a nullable string for rollback.

## Pattern source
`migration/src/m0001_initial/mod.rs` — `#[derive(DeriveMigrationName)] pub struct Migration;`,
`#[async_trait::async_trait] impl MigrationTrait for Migration { async fn up / async fn down }`,
schema statements built with `Table::...().to_owned()` and `.await`, Iden enums via `#[derive(DeriveIden)]`.

## Symbol dedup decision
Search `migration/` for an `Advisory` Iden enum. m0001 likely declares a private `Advisory` enum inside its module.
Decision: declare a local `Advisory { Table, Status }` Iden enum in m0002 rather than exporting m0001's enum. Rationale:
SeaORM migrations are intended to be immutable snapshots; coupling m0002 to m0001's identifiers would mean edits to
m0001 could silently change m0002. Stated in the commit body. (If CONVENTIONS.md mandates a shared Iden module, follow it instead.)

## Full content

```rust
//! Migration that drops the deprecated `status` column from the `advisory` table.
//!
//! The column was superseded by the `severity` enum field and is no longer read or
//! written by any service or entity code.

use sea_orm_migration::prelude::*;

/// Drops `advisory.status`; rollback re-adds it as a nullable string column.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Removes the deprecated `status` column from the `advisory` table.
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
    ///
    /// Data previously stored in the column is not restored.
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
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}

#[cfg(test)]
mod tests {
    use crate::Migrator;
    use sea_orm::{ConnectionTrait, DatabaseBackend, Statement};
    use sea_orm_migration::MigratorTrait;

    /// Returns `(data_type, is_nullable)` for `advisory.status`, or `None` if the column does not exist.
    async fn status_column(db: &sea_orm::DatabaseConnection) -> Option<(String, String)> {
        let row = db
            .query_one(Statement::from_string(
                DatabaseBackend::Postgres,
                "SELECT data_type, is_nullable FROM information_schema.columns \
                 WHERE table_name = 'advisory' AND column_name = 'status'",
            ))
            .await
            .expect("information_schema query");
        row.map(|r| {
            (
                r.try_get::<String>("", "data_type").unwrap(),
                r.try_get::<String>("", "is_nullable").unwrap(),
            )
        })
    }

    /// Verifies that applying all migrations removes the `status` column from `advisory`.
    #[tokio::test]
    async fn test_up_drops_status_column() {
        // Given a fresh test database
        let db = test_db().await; // project's PostgreSQL test-DB bootstrap helper (per CONVENTIONS.md)

        // When all migrations are applied
        Migrator::up(&db, None).await.expect("migrate up");

        // Then advisory.status no longer exists
        assert_eq!(status_column(&db).await, None);
    }

    /// Verifies that rolling back m0002 re-adds `status` as a nullable varchar column.
    #[tokio::test]
    async fn test_down_readds_status_column_as_nullable_string() {
        // Given a database with all migrations applied
        let db = test_db().await;
        Migrator::up(&db, None).await.expect("migrate up");

        // When the latest migration (m0002) is rolled back
        Migrator::down(&db, Some(1)).await.expect("migrate down");

        // Then advisory.status exists as a nullable character varying column
        assert_eq!(
            status_column(&db).await,
            Some(("character varying".to_string(), "YES".to_string()))
        );
    }

    /// Verifies that advisory entity queries still work after the column is dropped.
    #[tokio::test]
    async fn test_advisory_queries_work_after_drop() {
        // Given a migrated database with one inserted advisory
        let db = test_db().await;
        Migrator::up(&db, None).await.expect("migrate up");
        let inserted = insert_test_advisory(&db).await; // via entity::advisory::ActiveModel

        // When listing advisories through the entity
        let found = entity::advisory::Entity::find().all(&db).await.expect("query advisories");

        // Then the inserted advisory is returned with its values intact
        assert_eq!(found, vec![inserted]);
    }
}
```

Notes:
- `test_db()` / `insert_test_advisory()` are placeholders for the project's existing test-DB bootstrap and fixture helpers
  (to be located in Step 4 via `search_for_pattern` and reused rather than reimplemented). If `migration` lacks a
  dev-dependency on `entity`/`tokio`, that would require touching `migration/Cargo.toml` (out of scope) — in that case
  test #3 is covered by running the existing `tests/api/advisory.rs` integration suite against the migrated schema,
  and the Cargo.toml change is flagged for user approval rather than made silently.
