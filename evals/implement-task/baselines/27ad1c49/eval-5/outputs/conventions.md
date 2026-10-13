# Conventions Discovered from Sibling Analysis

## Source

Conventions extracted from sibling analysis of existing code in the trustify-backend
repository, focusing on the migration and entity modules.

## Migration Conventions

Derived from `migration/src/m0001_initial/mod.rs` (the only existing sibling migration):

- **Module structure**: each migration lives in its own subdirectory under `migration/src/` named `m<NNNN>_<descriptive_name>/mod.rs`
- **Naming**: migration directories use sequential numbering with zero-padded 4-digit prefix (e.g., `m0001_`, `m0002_`)
- **Trait implementation**: each migration implements `MigrationName` (returning the directory name as a string) and `MigrationTrait` (with `up` and `down` async methods)
- **Return type**: migration methods return `Result<(), DbErr>`
- **Async pattern**: uses `#[async_trait::async_trait]` attribute on the `MigrationTrait` impl
- **Schema manager**: both `up` and `down` receive `&SchemaManager` and use its builder methods
- **Registration**: migrations are registered in `migration/src/lib.rs` via `Box::new(<module>::Migration)` entries in a `vec![]` returned by the `migrations()` function
- **Local Iden enums**: migrations define their own `#[derive(Iden)] enum` for table and column identifiers rather than importing from the entity crate, keeping migrations self-contained

## Entity Conventions

Derived from `entity/src/advisory.rs` and sibling entity files:

- **Framework**: SeaORM entities with `#[derive(DeriveEntityModel)]` and related derives
- **Column naming**: columns use snake_case identifiers in the `Column` enum
- **Table naming**: table names match the struct name in lowercase

## General Rust Conventions

Derived from the overall repository structure:

- **Module pattern**: each domain area follows `model/ + service/ + endpoints/` structure
- **Error handling**: handlers use `Result<T, AppError>` with `.context()` wrapping
- **Naming**: `verb_noun` pattern for functions
- **Testing**: integration tests in `tests/api/` directory, use `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
- **Framework**: Axum for HTTP, SeaORM for database ORM

## Test Conventions

Derived from `tests/api/advisory.rs` and sibling test files:

- **Test location**: integration tests live in `tests/api/` with one file per domain entity
- **Assertion style**: `assert_eq!` for status code checks, value-based assertions on response body fields
- **Database**: tests hit a real PostgreSQL test database (not mocked)
- **Test naming**: `test_<verb>_<noun>` pattern (e.g., `test_list_advisories`, `test_get_advisory`)

## Conventions Applied to This Task

1. New migration directory: `migration/src/m0002_drop_advisory_status/mod.rs` (sequential numbering after m0001)
2. Implement both `MigrationName` and `MigrationTrait` with async up/down
3. Use local `#[derive(Iden)] enum Advisory` for table/column identifiers
4. Register with `Box::new(m0002_drop_advisory_status::Migration)` in lib.rs vec
5. Doc comments on all public symbols (skill guidance, applied regardless of sibling pattern)
