# Conventions Discovered (Sibling Analysis)

Siblings analyzed: `migration/src/m0001_initial/mod.rs`, `migration/src/lib.rs` (migration
registration), plus repo-level conventions from `repo-backend.md` / `CONVENTIONS.md` and
`tests/api/advisory.rs` for test style.

## Naming
- Migration modules: `mNNNN_<snake_case_description>/mod.rs`, zero-padded 4-digit sequence
  (`m0001_initial` -> next is `m0002_drop_advisory_status`).
- Each migration exposes a unit struct named `Migration` deriving `DeriveMigrationName`
  (migration name derived from module path).
- Table/column identifiers via a `#[derive(DeriveIden)] enum <Entity> { Table, <Column>... }`,
  PascalCase variants mapping to snake_case SQL names.

## Module structure / registration
- Each migration lives in its own directory module under `migration/src/`.
- `migration/src/lib.rs` declares `mod mNNNN_...;` and lists `Box::new(mNNNN_...::Migration)`
  in `MigratorTrait::migrations()` `vec![]`, in chronological order.
- Imports: `use sea_orm_migration::prelude::*;` as the single glob import in migrations.

## API / trait patterns
- `#[async_trait::async_trait] impl MigrationTrait for Migration` with
  `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` and matching `down`.
- Schema changes via `SchemaManager` builder API (`manager.create_table(...)`,
  `manager.alter_table(Table::alter()...to_owned())`), not raw SQL.
- `down` must reverse `up` to allow rollback.

## Error handling
- Migrations return `Result<(), DbErr>` and propagate the `SchemaManager` future result directly
  (no `.context()` — that `AppError` + `.context()` convention applies to HTTP handlers/services,
  not migrations).

## Tests
- Integration tests in `tests/api/` run against a real PostgreSQL test database.
- Status assertions use `assert_eq!(resp.status(), StatusCode::OK)`.
- Async tests use `#[tokio::test]`.
- Skill-guidance overrides applied (recorded deviations from siblings):
  - Every test function gets a `///` doc comment and Given/When/Then comments, regardless of
    sibling style.
  - Value-based assertions (exact `information_schema` column metadata) instead of
    existence/length-only checks.
  - Parameterized tests not introduced (up and down tests differ in setup/assertions, and
    no `rstest` usage observed in siblings).

## Documentation
- New public structs/enums/functions carry a one-line `///` doc comment; module-level `//!`
  doc describes the migration purpose.

## Convention conflicts
- None between the task description and sibling conventions. The Implementation Notes'
  `TableAlterStatement` / `ColumnDef::new(...).string().null()` usage matches SeaORM
  migration conventions.
- Scope note (not a conflict): Test Requirement 3 ("existing advisory queries still work")
  is satisfied by running the existing `tests/api/advisory.rs` suite unchanged; no new file
  under `tests/` is planned since none is listed in Files to Create.
