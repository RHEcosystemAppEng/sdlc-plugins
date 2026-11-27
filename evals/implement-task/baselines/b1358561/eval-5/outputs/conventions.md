# Conventions discovered (Step 4 sibling analysis)

Sources: `migration/src/m0001_initial/mod.rs` (the primary sibling, named in the Implementation Notes), `migration/src/lib.rs`, `entity/src/advisory.rs`, the "Key Conventions" in the repo structure, and `CONVENTIONS.md` (repo root, read for CI commands and rules).

## Naming
- Migration modules are `mNNNN_<snake_case_description>/mod.rs`, zero-padded to 4 digits and sequential. The next one is `m0002_drop_advisory_status`.
- The migration struct is always named `Migration` and derives `DeriveMigrationName`, so the name comes from the module.
- Table and column identifiers use an Iden enum named after the table in PascalCase (`Advisory`), with a `Table` variant and PascalCase column variants (`Status`).

## Module structure and registration
- Each migration is a self-contained directory module that imports `sea_orm_migration::prelude::*`.
- `migration/src/lib.rs` declares each module with `mod mNNNN_...;` and lists `Box::new(mNNNN_...::Migration)` in `Migrator::migrations()` in chronological order.
- Iden enums are declared per migration, not shared across migrations.

## API and patterns
- `#[async_trait::async_trait] impl MigrationTrait for Migration` provides both `up` and `down`.
- Signatures are `async fn up/down(&self, manager: &SchemaManager) -> Result<(), DbErr>`.
- Schema changes use the SeaQuery builders (`Table::create()`, `Table::alter()`, `ColumnDef::new(..)`), end with `.to_owned()`, and are passed to `manager.<op>(..).await`. There is no raw SQL.

## Error handling
- Migrations return `DbErr` directly and propagate with the builder's `.await` result. There is no `AppError` or `.context()`, which applies only to HTTP handlers.
- Application code (handlers and services) uses `Result<T, AppError>` with `.context()`. It does not apply here.

## Framework and architecture
- Axum for HTTP, SeaORM for DB, PostgreSQL.
- Domain modules follow `model/ + service/ + endpoints/`. Entities live in `entity/src/<table>.rs`. Advisory now uses the `severity` enum field (AdvisorySummary), not `status`.

## Testing
- Integration tests live in `tests/api/*.rs` and hit a real PostgreSQL test database.
- Status assertions use `assert_eq!(resp.status(), StatusCode::OK)`.
- Siblings do not use parameterized tests (`rstest`), so none are introduced.
- Skill overrides recorded: every test gets a `///` doc comment and Given/When/Then comments. Assertions are value-based, comparing column name, data_type and nullability rather than counts.

## Verification
- CI commands are taken from the CONVENTIONS.md CI section; expected to include `cargo fmt --check`, `cargo clippy`, and `cargo test`.
- Per-crate tests are resolved via `cargo metadata`: `cargo test -p migration`, plus the advisory integration tests.

## Conflicts
- None between the task and the conventions. The task's suggested `Table::alter()...drop_column(...)` matches the SeaORM builder pattern in m0001.
