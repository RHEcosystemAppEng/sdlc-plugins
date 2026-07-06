# Conventions Discovered from Sibling Analysis

## Source

Conventions derived from analyzing the existing codebase structure in `trustify-backend`, particularly the sibling migration `migration/src/m0001_initial/mod.rs` and the overall repository patterns documented in repo-backend.md and CONVENTIONS.md (if present).

## Migration Conventions

- **Directory structure**: Each migration lives in its own directory under `migration/src/`, named with a sequential prefix: `m0001_initial/`, `m0002_drop_advisory_status/`, etc. Each directory contains a `mod.rs` entry point.
- **Naming pattern**: Migration directories follow `m<NNNN>_<descriptive_name>` format with zero-padded sequential numbering.
- **Trait implementation**: Each migration implements `MigrationTrait` with `up` (apply) and `down` (rollback) async methods, and `MigrationName` with a `name()` method returning the module name as a string.
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding a module declaration (`mod m0002_...`) and appending `Box::new(m0002_...::Migration)` to the `vec![]` in the `migrations()` function.
- **Self-contained identifiers**: Each migration defines its own `#[derive(Iden)] enum` for table and column identifiers rather than importing from the `entity` crate. This ensures migrations remain stable even as entity definitions evolve.
- **Async trait**: Uses `#[async_trait::async_trait]` attribute on the `MigrationTrait` implementation.
- **SeaORM API**: Uses `SchemaManager` methods (`alter_table`, `create_table`, etc.) with builder pattern calls (`Table::alter().table(...).drop_column(...)...to_owned()`).

## General Project Conventions

- **Framework**: Axum for HTTP, SeaORM for database ORM and migrations.
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure.
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`.
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Test Conventions

- **Location**: Integration tests reside in `tests/api/` with one file per domain (e.g., `advisory.rs`, `sbom.rs`).
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization for response validation.
- **Database**: Tests run against a real PostgreSQL test database (not mocks).
- **Naming**: Test files are named after the domain entity they test (e.g., `tests/api/advisory.rs` for advisory endpoint tests).
