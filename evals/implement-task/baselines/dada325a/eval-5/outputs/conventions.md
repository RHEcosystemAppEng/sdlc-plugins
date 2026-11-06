# Conventions from sibling analysis — TC-9205

Siblings examined: `migration/src/m0001_initial/mod.rs` and `migration/src/lib.rs` (migration crate), `entity/src/advisory.rs` (the affected entity), and `tests/api/advisory.rs` (test style). Repo-level conventions come from `CONVENTIONS.md` and the repository overview.

## Naming
- Migration modules are named `mNNNN_<snake_case_description>/mod.rs` with zero-padded sequence numbers (`m0001_initial`), so the new one is `m0002_drop_advisory_status`.
- Each migration exposes a struct named `Migration`. The name comes from `#[derive(DeriveMigrationName)]`, which uses the module name.
- Iden enums are PascalCase and named after the table (`Advisory`), with variants `Table` plus PascalCase column names (`Status`).
- Function names are snake_case `verb_noun`.

## Module structure and registration
- Each migration lives in its own directory module and is declared with `mod mNNNN_...;` in `migration/src/lib.rs`.
- Migrations are registered in order in `Migrator::migrations()` as `Box::new(<module>::Migration)` inside `vec![]`. New entries are appended at the end.
- Imports use the `use sea_orm_migration::prelude::*;` glob.
- Iden enums are declared locally in each migration module and not shared across migrations, so each migration stays a self-contained snapshot.

## Migration API patterns
- `#[async_trait::async_trait] impl MigrationTrait for Migration` with both `up` and `down`.
- Signature: `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>`.
- Schema changes go through `manager.create_table / alter_table(...)` with builder statements ending in `.to_owned()` and awaited directly as the return value.
- `down` must reverse `up` so that rollback works.

## Error handling
- Migrations return `Result<(), DbErr>` and propagate SeaORM errors directly, with no `.context()` wrapping.
- Application code (handlers and services) uses `Result<T, AppError>` with `.context()`. That pattern does not apply to migrations.

## Framework
- Axum for HTTP and SeaORM for the database (PostgreSQL).
- Domain modules follow `model/ + service/ + endpoints/`. This task does not touch them.

## Test patterns
- Integration tests in `tests/api/*.rs` run against a real PostgreSQL test database.
- Status assertions use `assert_eq!(resp.status(), StatusCode::OK)`, i.e. `assert_eq!` against concrete expected values.
- Async tests use `#[tokio::test]`.
- The repo does not show parameterized tests (`rstest`), so none are introduced here. The two migration tests also differ in setup and assertions, so parameterizing them would not fit anyway.

## Skill guidance applied over sibling patterns
- Every new test function gets a `///` doc comment, plus `// Given` / `// When` / `// Then` sections for non-trivial tests. This applies even if the siblings don't do it.
- Assertions check values (exact column `data_type` and `is_nullable`, column absence) and not just counts.
- Every new public item gets a doc comment (module `//!`, `Migration`, `up`/`down`, and the `Advisory` iden enum).

## Branching/PR conventions (from the task and skill)
- The task branch is named after the Jira key (`TC-9205`) and created from the Target Branch `TC-9005` (the feature branch).
- The PR base is the Target Branch `TC-9005`, not `main`.
- Commits follow Conventional Commits with an `Implements TC-9205` footer and the `Assisted-by:` trailer.

## Convention conflicts
- None found between the task description and the sibling conventions.
- Scope note: Test Requirement (c), that advisory queries still work, would naturally go in `tests/api/advisory.rs`, which is not in Files to Modify. It is covered by re-running the existing suite, and any edit to that file would be flagged for user approval.
