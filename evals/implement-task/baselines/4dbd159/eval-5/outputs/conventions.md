# Discovered Conventions (from sibling analysis)

## Source: Repository Key Conventions (repo-backend.md)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders

## Source: Sibling Migration Analysis (m0001_initial/mod.rs)

The existing migration `m0001_initial/mod.rs` establishes the following conventions for migration files:

- **Migration trait**: Each migration implements `MigrationTrait` with `up` and `down` async methods
- **Migration name**: Implements `MigrationName` trait returning a string matching the module directory name
- **Module structure**: Each migration lives in its own subdirectory under `migration/src/` with a `mod.rs` file
- **Naming convention**: Migration directories follow `m<NNNN>_<descriptive_name>` pattern (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding `Box::new(<module>::Migration)` to the `migrations()` function's return vector
- **Iden enums**: SeaORM `Iden` derive macro is used for table and column identifiers
- **Rollback support**: Every `up` migration must have a corresponding `down` method for rollback

## Source: Entity Analysis (entity/src/advisory.rs)

- **Entity definitions**: SeaORM entity structs with `DeriveEntityModel` derive macro
- **Column mapping**: Each database column maps to a field in the entity struct
- **Verification note**: The `advisory.rs` entity no longer references `status` column, confirming it was already removed at the entity level -- the migration is safe to proceed

## Discovered Test Conventions (from sibling test analysis)

- **Assertion style**: Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Error cases**: Endpoint tests include status code assertions for error scenarios (e.g., `StatusCode::NOT_FOUND`)
- **Test database**: Tests run against a real PostgreSQL test database (not mocked)
- **Migration testing**: Migration tests would verify both `up` (column dropped) and `down` (column restored) by running the migration and querying the schema

## CONVENTIONS.md

A `CONVENTIONS.md` file exists at the repository root. It should be read during implementation for:
- CI check commands to run before committing
- Code generation commands that may produce artifacts to commit
- Additional naming rules, directory structure, or code pattern requirements
