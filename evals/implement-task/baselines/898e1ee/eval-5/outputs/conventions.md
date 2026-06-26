# Conventions Discovered from Sibling Analysis

## Source of conventions

Conventions were identified from two sources:
1. **Repository Key Conventions** (from `repo-backend.md`): explicit project-level conventions
2. **Sibling analysis** of `migration/src/m0001_initial/mod.rs`: the only existing migration module, serving as the direct sibling for the new migration

## Production code conventions (from sibling analysis of m0001_initial)

- **Migration struct pattern**: Each migration module defines a `Migration` struct that derives `DeriveMigrationName` and implements `MigrationTrait`
- **Async trait**: Migration methods use `#[async_trait::async_trait]` for async `up` and `down` methods
- **Method signatures**: Both `up` and `down` take `&self` and `&SchemaManager` and return `Result<(), DbErr>`
- **Table/column references**: Use SeaORM's `Iden` derive macro on enums to define table and column identifiers (e.g., `Advisory::Table`, `Advisory::Status`)
- **Migration registration**: Migrations are registered in `migration/src/lib.rs` via `Box::new(<module>::Migration)` inside a `vec![]` returned by the `migrations()` function
- **Module declaration**: Each migration directory is declared as a module in `lib.rs` with `mod <migration_name>;`
- **Directory naming**: Migration directories follow `m<NNNN>_<descriptive_name>` format (e.g., `m0001_initial`, `m0002_drop_advisory_status`)

## Project-level conventions (from repository documentation)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Test conventions (from sibling analysis of tests/api/)

- **Assertion style**: Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test location**: Integration tests live in `tests/api/` with one file per domain (e.g., `advisory.rs`, `sbom.rs`)
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern
- **Database**: Tests use a real PostgreSQL test database (not mocks)

## Conventions applied to this task

- The new migration in `m0002_drop_advisory_status/mod.rs` follows the exact struct and trait pattern from `m0001_initial/mod.rs`
- Registration in `lib.rs` follows the existing `mod` + `Box::new()` pattern
- Directory naming follows the `m<NNNN>_<name>` convention with sequential numbering
- Documentation comments are added to the migration struct (code quality practice from SKILL.md)
