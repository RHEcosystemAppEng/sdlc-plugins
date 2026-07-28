# Discovered Conventions (from sibling analysis)

## Production Code Conventions

Conventions discovered by analyzing the existing migration module `migration/src/m0001_initial/mod.rs` and the broader repository structure.

### Migration Conventions

- **Module structure**: Each migration lives in its own subdirectory under `migration/src/` named `m<NNNN>_<descriptive_name>/`, containing a `mod.rs` file (e.g., `m0001_initial/mod.rs`).
- **Trait implementation**: Every migration module implements `MigrationTrait` from SeaORM, which requires `up` and `down` async methods.
- **Migration registration**: Migrations are registered in `migration/src/lib.rs` by adding the module to a `vec![]` in the `migrations()` function. Each migration is listed in order.
- **Naming pattern**: Migration directory names follow zero-padded sequential numbering: `m0001_`, `m0002_`, etc., with a snake_case description suffix.
- **Schema operations**: Migrations use SeaORM's schema manager for DDL operations (`manager.alter_table(...)`, `manager.create_table(...)`, etc.) rather than raw SQL.
- **Rollback support**: Every migration's `down` method must reverse the `up` operation to support rollback.

### General Code Conventions

- **Framework**: Axum for HTTP, SeaORM for database ORM.
- **Module pattern**: Domain modules follow a `model/ + service/ + endpoints/` three-layer structure.
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping for error enrichment.
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`.
- **Entity definitions**: SeaORM entities live in `entity/src/`, one file per table (e.g., `advisory.rs`, `sbom.rs`).

## Test Conventions

Conventions discovered by analyzing test files in `tests/api/`.

- **Test location**: Integration tests reside in `tests/api/` with one file per domain entity (e.g., `advisory.rs`, `sbom.rs`).
- **Assertion style**: Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- **Test database**: Tests run against a real PostgreSQL test database (not mocks).
- **Test naming**: Tests follow `test_<entity>_<scenario>` naming pattern.
- **Error cases**: Endpoint tests include coverage for 404 (not found) responses.

## Commit Conventions

- **Format**: Conventional Commits specification: `<type>[optional scope]: <description>`
- **Footer**: Must include `Implements <JIRA-ID>`
- **Trailer**: Must include `Assisted-by: Claude Code`
