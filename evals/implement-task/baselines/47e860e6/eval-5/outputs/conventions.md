# Conventions Discovered (sibling analysis)

Siblings analysed:
- `migration/src/m0001_initial/mod.rs`, the only existing migration and the main sibling for the new file
- `migration/src/lib.rs`, the migrator registry
- `entity/src/advisory.rs`, the SeaORM entity for the affected table
- `tests/api/advisory.rs` and `tests/api/sbom.rs`, the test pattern siblings
- `CONVENTIONS.md` at the repo root, plus the repo "Key Conventions" summary

In a real run these would be inspected with `mcp__serena_backend__get_symbols_overview` and `find_symbol`.

## Naming
- Migration modules are named `m<NNNN>_<snake_case_description>/mod.rs`, with a zero-padded sequence number. This gives `m0002_drop_advisory_status`.
- Every migration struct is called `Migration` and derives `DeriveMigrationName`. The name comes from the module path.
- Iden enums are named after the table (`Advisory`), with variant `Table` plus PascalCase column variants (`Status`).
- Functions use snake_case `verb_noun`. Test names use the `test_` prefix and describe the behaviour.

## Module structure / imports
- Each migration has its own directory containing a `mod.rs`.
- Migrations import with `use sea_orm_migration::prelude::*;`.
- `lib.rs` declares each migration with a private `mod mNNNN_...;` and registers it in `MigratorTrait::migrations()` as `Box::new(<module>::Migration)`, in chronological order.
- Trait impls use `#[async_trait::async_trait]`.

## Migration patterns
- Implement `MigrationTrait` with both `up` and `down`. `down` must reverse `up` so rollback works.
- Use the SchemaManager builders (`Table::alter()`, `ColumnDef::new(...)`, `.to_owned()`) rather than raw SQL.
- Iden enums are declared per migration with `#[derive(DeriveIden)]`, so a migration does not depend on another migration's or the entity's identifiers.

## Error handling
- Migration methods return `Result<(), DbErr>` and propagate the `SchemaManager` future result directly. No `.context()` is used there.
- Application handlers (not touched here) return `Result<T, AppError>` with `.context()` wrapping.

## Testing
- Integration tests in `tests/api/` run against a real PostgreSQL test database.
- Assertion style is `assert_eq!` (e.g. `assert_eq!(resp.status(), StatusCode::OK)`).
- Async tests use `#[tokio::test]`.
- Siblings do not appear to use parameterized tests (`rstest`), so none are introduced. The two migration tests also differ in setup and assertions, so the Meszaros heuristic favours separate tests anyway.
- **Skill guidance overrides sibling patterns.** Every test gets a `///` doc comment and given-when-then comments, and assertions compare values (column type and nullability) rather than lengths. Siblings may not document their tests; this deviation is intentional.

## Documentation
- New public items get `///` doc comments and the module gets a `//!` header. This comes from the skill's quality rule, applied even where siblings are sparse.

## CI / verification (from CONVENTIONS.md)
- Expected CI checks are `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings` and `cargo check`, plus `cargo test -p migration` (a mandatory per-crate test run for Rust). A failure in any of these is a hard stop before commit.

## Convention conflicts
- None between the task and the sibling conventions. The Implementation Notes match the m0001 pattern.
- Scope note: the task's Test Requirements imply test code, but no test file is listed. Tests are placed inside the new migration file. A new test in `tests/api/advisory.rs`, or any `migration/Cargo.toml` dev-dependency changes, would need user approval.
