# Conventions Discovered (sibling analysis)

Sources: `migration/src/m0001_initial/mod.rs` and `migration/src/lib.rs` (direct siblings), `entity/src/advisory.rs`, `tests/api/advisory.rs`, the repo "Key Conventions", and `CONVENTIONS.md` (read at repo root; its CI commands drive Step 9).

## Migration structure
- One directory per migration, `migration/src/mNNNN_<snake_case_description>/mod.rs`, with a zero-padded 4-digit sequence number. The next one is `m0002_drop_advisory_status`.
- Each migration defines `#[derive(DeriveMigrationName)] pub struct Migration;`.
- It implements `MigrationTrait` via `#[async_trait::async_trait]`, with `async fn up/down(&self, manager: &SchemaManager) -> Result<(), DbErr>`.
- Imports: a single `use sea_orm_migration::prelude::*;`.
- Schema changes go through `SchemaManager` builder APIs (`Table::alter()`, `ColumnDef::new(..)`, `.to_owned()`, `.await`), not raw SQL.
- Table and column identifiers are declared as a local `#[derive(DeriveIden)] enum <Table> { Table, <Column>... }` inside each migration. Migrations stay self-contained and do not import identifiers from other migrations or from `entity/`.

## Registration
- `migration/src/lib.rs` declares `mod mNNNN_...;` per migration, and `Migrator::migrations()` returns `vec![Box::new(mNNNN_...::Migration), ...]` in chronological order. Append new migrations at the end.

## Naming
- snake_case modules and functions, PascalCase types and enum variants, and `verb_noun` descriptive names (`drop_advisory_status`).

## Error handling
- Migrations return `Result<(), DbErr>` directly (propagating SeaORM errors). The `Result<T, AppError>` + `.context()` convention applies to HTTP handlers and services, not migrations.

## Entities / ORM
- SeaORM entities live in `entity/src/<table>.rs`. The `advisory` entity uses a `severity` enum and (per the task) no longer has `status`; this is to be verified with Serena before implementing.

## Testing
- Integration tests in `tests/api/*.rs` run against a real PostgreSQL test DB.
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)`, i.e. `assert_eq!` with concrete values.
- Applied skill overrides (these take precedence over sibling patterns):
  - every test function gets a `///` doc comment
  - non-trivial tests get `// Given / // When / // Then` sections
  - value-based assertions (column nullability/type values), not just existence or length checks
  - parameterized tests not used: the two cases (up vs down) differ in setup and assertions, and siblings don't use `rstest`.

## Documentation
- Every new public or derived type gets a `///` doc comment (struct `Migration`, enum `Advisory`, and the `up`/`down` methods).

## Workflow conventions
- Branch name = Jira key (`TC-9205`), created from the Target Branch (`TC-9005` feature branch).
- PR base = Target Branch (`--base TC-9005`).
- Conventional Commits with the `Implements TC-9205` footer and the `Assisted-by` trailer.

## Conflicts noted
- None between the task and the sibling conventions. One scope consideration: test dev-dependencies in `migration/Cargo.toml` (if missing) and new tests in `tests/api/advisory.rs` are outside Files to Modify/Create. They would be flagged for user approval, not silently added.
