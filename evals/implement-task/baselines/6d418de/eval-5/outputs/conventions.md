# Conventions Discovered from Sibling Analysis

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

1. **Module structure**: Each migration lives in its own directory under `migration/src/` following the naming pattern `m<NNNN>_<snake_case_description>/mod.rs` (e.g., `m0001_initial/mod.rs`, `m0002_drop_advisory_status/mod.rs`).

2. **Trait implementation**: Every migration module implements `MigrationTrait` from SeaORM, which requires two async methods:
   - `up(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- applies the migration
   - `down(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- rolls back the migration

3. **Migration registration**: All migration modules are declared in `migration/src/lib.rs` and added to the `vec![]` returned by the `migrations()` function in order.

4. **SeaORM patterns**: Migrations use SeaORM's schema manager API:
   - `TableCreateStatement` for creating tables
   - `TableAlterStatement` for altering tables (add/drop columns)
   - Entity enum identifiers (e.g., `Advisory::Table`, `Advisory::Status`) for referencing tables and columns

5. **Rollback safety**: The `down` method must fully reverse the `up` method. For column drops, this means re-adding the column with its original type and nullability (nullable to avoid breaking existing data on rollback).

## Entity Conventions (from `entity/src/advisory.rs`)

6. **SeaORM entity definition**: Each entity file defines a SeaORM `Entity` with a corresponding `Column` enum that lists all active columns. The `advisory.rs` entity no longer references a `status` column -- it uses a `severity` enum field instead, confirming the column is safe to drop.

## General Rust Conventions

7. **Framework**: Axum for HTTP, SeaORM for database ORM.
8. **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping.
9. **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure.
10. **Testing**: Integration tests live in `tests/api/` and hit a real PostgreSQL test database; tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Commit Conventions

11. **Conventional Commits**: `<type>[optional scope]: <description>` format.
12. **Jira footer**: `Implements <JIRA-ID>` in commit footer.
13. **AI trailer**: `Assisted-by: Claude Code` via `--trailer`.

## Branch Conventions

14. **Branch naming**: Task branches named after Jira issue ID (e.g., `TC-9205`).
15. **Feature branch targeting**: When Target Branch is a feature issue ID, PR targets that branch via `--base <feature-branch>`.
