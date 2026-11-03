# Conventions Discovered (sibling analysis) — trustify-backend, TC-9205

Sources: `migration/src/m0001_initial/mod.rs` (direct sibling), `migration/src/lib.rs`, `entity/src/advisory.rs`,
repo "Key Conventions" section, `CONVENTIONS.md` (repo root — to be read via `serena_backend`), `tests/api/advisory.rs`.

## Naming
- Migration modules: `mNNNN_<snake_case_description>/mod.rs`, zero-padded 4-digit sequence → next is `m0002_drop_advisory_status`.
- Migration struct is always named `Migration`, deriving `DeriveMigrationName` (name derived from the module path).
- Table/column identifiers: PascalCase Iden enum named after the table (`Advisory`) with `Table` + column variants (`Status`).
- Task branch named after the Jira key (`TC-9205`); feature branch named after the feature key (`TC-9005`).

## Module structure / registration
- Each migration is a directory module declared in `migration/src/lib.rs` (`mod m0001_initial;`).
- Registered in order in `Migrator::migrations()` as `Box::new(<module>::Migration)` inside `vec![]`.
- `use sea_orm_migration::prelude::*;` as the single prelude import.

## API design / migration pattern
- `#[async_trait::async_trait] impl MigrationTrait for Migration` with `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` and matching `down`.
- Schema statements built fluently (`Table::alter().table(..).drop_column(..)`) terminated with `.to_owned()` and passed to `manager.<op>(..).await`.
- `down` must reverse `up` (here: re-add `status` as `ColumnDef::new(..).string().null()`).
- Migrations are self-contained (local Iden enums) — not importing identifiers from other migrations.

## Error handling
- Migrations return `Result<(), DbErr>` and propagate the SeaORM result directly (no `.context()` in migration code).
- Application handlers/services use `Result<T, AppError>` with `.context()` (common/src/error.rs) — not applicable to this change.

## Tests
- Integration tests hit a real PostgreSQL test database (`tests/api/`).
- Assertion style: `assert_eq!` (e.g. `assert_eq!(resp.status(), StatusCode::OK)`).
- Sibling tests do not appear to use parameterized tests (rstest) → not introduced; the three tests differ in setup/assertions anyway.
- Skill guidance applied over sibling patterns: every test has a `///` doc comment and `// Given / // When / // Then` sections; assertions are value-based (column `data_type`/`is_nullable`, returned advisory equality) rather than existence/count-only.

## Documentation
- New public symbols get `///` doc comments; module gets a `//!` header describing the migration.

## Verification
- CI commands extracted from `CONVENTIONS.md` (expected: `cargo fmt --check`, `cargo clippy -D warnings`, `cargo check`) plus `cargo test -p migration` (Rust module-level test requirement) — any non-zero exit is a hard stop before commit.

## Conflicts
- None between the task description and sibling conventions. The Implementation Notes' `drop_column` / `ColumnDef::new(Advisory::Status).string().null()` match the SeaORM pattern used by m0001.
