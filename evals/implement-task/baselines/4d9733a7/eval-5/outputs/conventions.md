# Conventions Discovered from Sibling Analysis

## Source

Conventions discovered by analyzing the repository structure described in `repo-backend.md`, the existing migration module `migration/src/m0001_initial/mod.rs`, the entity definitions in `entity/src/`, and the project's key conventions section.

## Production Code Conventions

### Migration conventions (from `m0001_initial/mod.rs` sibling)

- **Module naming**: Migrations follow the `m<NNNN>_<snake_case_description>` pattern (e.g., `m0001_initial`, `m0002_drop_advisory_status`). Each migration lives in its own directory under `migration/src/` with a `mod.rs` file.
- **Struct pattern**: Each migration module exports a `Migration` unit struct that implements both `MigrationName` and `MigrationTrait`.
- **MigrationName**: Returns a string identifier matching the module directory name.
- **MigrationTrait**: Requires both `up` (apply) and `down` (rollback) async methods returning `Result<(), DbErr>`.
- **Self-contained identifiers**: Migration modules define their own `#[derive(Iden)]` enums for table and column names rather than importing from the entity crate. This ensures migrations remain stable even if entity definitions evolve.
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding `Box::new(<module>::Migration)` to the `vec![]` returned by the `migrations()` function, in sequential order.

### Database and ORM conventions

- **Framework**: SeaORM for all database operations (migrations, entities, queries).
- **Schema changes**: Use SeaORM's `TableAlterStatement` API for column additions, drops, and modifications. The pattern is `manager.alter_table(Table::alter().table(...).drop_column(...).to_owned()).await`.
- **Entity pattern**: SeaORM entities are defined in `entity/src/` with one file per table (e.g., `advisory.rs`, `sbom.rs`).

### Error handling conventions

- **Service and handler code**: All handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation.
- **Migration code**: Migrations return `Result<(), DbErr>` directly using the `?` operator on SeaORM manager calls.

### Module structure conventions

- **Domain modules**: Each domain follows `model/ + service/ + endpoints/` structure under `modules/fundamental/src/`.
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`).

### Response and API conventions

- **List endpoints**: Return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`.

## Test Conventions

### Test structure (from `tests/api/` siblings)

- **Test location**: Integration tests live in `tests/api/` with one file per domain (e.g., `advisory.rs`, `sbom.rs`, `search.rs`).
- **Test database**: Tests hit a real PostgreSQL test database (not mocks).
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code validation, followed by body deserialization for content checks.
- **Naming**: Test functions follow `test_<entity>_<scenario>` pattern.

### Migration-specific test conventions

- Migration tests should verify both `up` (forward migration) and `down` (rollback) execute without errors against the test database.
- Post-migration queries should be run to confirm existing data access patterns (e.g., advisory list/get endpoints) continue to work after the column is dropped.

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` file at the root (`trustify-backend/CONVENTIONS.md`). In a real implementation, this file would be read and its conventions would take precedence over the sibling-analysis conventions documented above. Any CI check commands found in `CONVENTIONS.md` would be extracted and run during the self-verification step (Step 9).
