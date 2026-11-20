# Conventions discovered (sibling analysis)

Siblings analysed (via `mcp__serena_backend__get_symbols_overview` / `find_symbol`, Read fallback):
- `migration/src/m0001_initial/mod.rs` — only existing migration (primary sibling for the new file)
- `migration/src/lib.rs` — migration registry
- `entity/src/advisory.rs` — advisory entity (to confirm `status` is gone)
- `tests/api/advisory.rs` — test conventions
- `CONVENTIONS.md` at repo root — authoritative conventions and CI commands

## Naming
- Migration modules: `mNNNN_<snake_case_description>/mod.rs`, zero-padded 4-digit sequence
  (`m0001_initial` → new `m0002_drop_advisory_status`).
- Migration struct is always named `Migration`, deriving `DeriveMigrationName` (name derived from module path).
- Table/column identifiers: `DeriveIden` enum named after the table in PascalCase (`Advisory`) with a
  `Table` variant plus PascalCase column variants (`Status`).
- Rust naming: snake_case functions/modules, PascalCase types.

## Module structure / registration
- Each migration lives in its own directory module; `lib.rs` declares `mod mNNNN_...;` and adds
  `Box::new(mNNNN_...::Migration)` to `migrations()` vec in chronological order.
- Migrations import `sea_orm_migration::prelude::*` and do not depend on the `entity` crate
  (identifier enums are local and frozen).

## Migration API pattern
- `#[async_trait::async_trait] impl MigrationTrait for Migration` with `up` and `down`, both
  `async fn(&self, manager: &SchemaManager) -> Result<(), DbErr>`.
- Schema changes via `manager.create_table/alter_table(... .to_owned()).await`, builder style.
- `down` must reverse `up` (here: re-add column as nullable string).

## Error handling
- Migrations return `Result<(), DbErr>` directly, propagating with `.await` (no `AppError`/`.context()`
  — that convention applies to HTTP handlers/services: `Result<T, AppError>` with `.context()`).

## Project-wide (from repo-backend.md / CONVENTIONS.md)
- Framework: Axum (HTTP), SeaORM (DB), PostgreSQL.
- Domain modules follow `model/ + service/ + endpoints/`; list endpoints return `PaginatedResults<T>`;
  shared query helpers in `common/src/db/query.rs` (not relevant to this task).

## Test conventions
- Integration tests in `tests/api/` run against a real PostgreSQL test database.
- Assertion style: `assert_eq!` (e.g., `assert_eq!(resp.status(), StatusCode::OK)`).
- Async tests with `#[tokio::test]`.
- Skill-imposed standards applied even if siblings lack them: `///` doc comment on every test,
  Given/When/Then comments in non-trivial tests, value-based assertions (assert column type and
  nullability, not just presence).
- Parameterized tests (`rstest`): not introduced — the two migration tests differ in action and
  assertion, and siblings do not show parameterized usage.

## Conflicts / notes
- No conflict between task Implementation Notes and sibling conventions.
- Test Requirements imply tests but no test file is listed in Files to Create/Modify; tests are
  placed in-module in the new migration file (in scope). Any test in the `tests/` crate would be
  flagged for user approval as out of scope. "Existing advisory queries still work" is verified by
  running the existing `tests/api/advisory.rs` suite unchanged.
- CI commands to run in Step 9 are taken from CONVENTIONS.md's CI checks section (typically
  `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`); plus
  `cargo test -p migration` per the Rust module-level test requirement.
