# Conventions discovered (Step 4 sibling analysis)

Siblings analyzed:
- `migration/src/m0001_initial/mod.rs`, the direct sibling migration
- `migration/src/lib.rs`, the Migrator registration
- `entity/src/advisory.rs`, the advisory entity (to check that `status` is unused)
- the repo-level conventions in `repo-backend.md`, plus `CONVENTIONS.md` at the repo root (would be read through `serena_backend` / Read)

## Naming
- Migration modules use `mNNNN_<snake_case_description>/mod.rs` with a zero-padded sequence. The new module is `m0002_drop_advisory_status`.
- Each migration module exposes a struct named `Migration`, which `lib.rs` refers to as `<module>::Migration`.
- Table and column identifiers are an Iden enum named after the table (`Advisory`), with a `Table` variant plus PascalCase column variants (`Status`).

## Structure and module organization
- One directory per migration, holding a single `mod.rs`.
- `lib.rs` declares each migration with a private `mod` and lists them in chronological order in `Migrator::migrations()` as `Box::new(...)`.
- Imports come from `use sea_orm_migration::prelude::*;` (a single prelude glob).

## Migration pattern
- `#[derive(DeriveMigrationName)] pub struct Migration;`
- `#[async_trait::async_trait] impl MigrationTrait for Migration` with both `up` and `down` implemented. `down` must be a true inverse for rollback.
- Schema changes go through `manager.create_table/alter_table(Table::...().to_owned()).await`, using the builder API rather than raw SQL.
- Identifiers use `#[derive(DeriveIden)]` enums, declared locally in each migration so that migrations stay immutable snapshots.

## Error handling
- Migration functions return `Result<(), DbErr>` and propagate the `SchemaManager` future result directly. There is no `.context()` wrapping here. `Result<T, AppError>` with `.context()` is the convention for HTTP handlers and does not apply to migrations.

## Framework / stack
- SeaORM (and `sea_orm_migration`) on PostgreSQL. Axum for HTTP, which this task does not touch.

## Testing
- Integration tests live in `tests/api/*.rs` and run against a real PostgreSQL test DB. The assertion style is `assert_eq!(resp.status(), StatusCode::OK)`.
- The siblings show no parameterized tests (`rstest`), so none are introduced. The two migration tests (up and down) have different actions and assertions anyway.
- Skill override: every new test gets a `///` doc comment and Given/When/Then section comments, even if sibling tests lack them. Assertions check the actual column presence or absence rather than counts.

## Documentation
- Skill quality rule: every new public struct, enum, and function gets a `///` doc comment, including the `Migration` struct, the `up`/`down` methods, and the `Advisory` Iden.

## Conflicts noted
- Test Requirements vs scope: the tests are required, but no test file is listed in Files to Create. Resolution: put the up/down tests in a `#[cfg(test)]` module inside the in-scope new file. Cover "existing advisory queries still work" by running the existing `tests/api/advisory.rs` unchanged. Any separate test file would be flagged for user approval in Step 9.
- No conflict between the Implementation Notes and the sibling conventions. The notes explicitly point to the m0001 pattern.
