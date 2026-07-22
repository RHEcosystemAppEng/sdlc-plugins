# Conventions Discovered from Sibling Analysis

## Source

Conventions discovered by analyzing the repository structure described in `repo-backend.md`, the existing migration pattern in `m0001_initial/mod.rs`, and the project's Key Conventions section.

## Production Code Conventions

### Migration Pattern (from `m0001_initial/mod.rs` sibling)
- **Structure**: Each migration lives in its own directory under `migration/src/` named `m<NNNN>_<description>/mod.rs`
- **Trait implementation**: Migrations implement `MigrationTrait` with async `up()` and `down()` methods
- **Naming macro**: Use `#[derive(DeriveMigrationName)]` for automatic migration name derivation
- **Async trait**: Use `#[async_trait::async_trait]` attribute on the `MigrationTrait` impl
- **Registration**: Each migration is registered in `migration/src/lib.rs` by adding `Box::new(<module>::Migration)` to the `migrations()` vec
- **Imports**: Use `sea_orm_migration::prelude::*` for all migration-related types
- **Local identifiers**: Define local `#[derive(Iden)]` enums for table/column references within the migration rather than importing from the entity crate (migrations must be self-contained)

### Framework Conventions (from Key Conventions)
- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping for error propagation
- **Module pattern**: Each domain follows `model/ + service/ + endpoints/` directory structure
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`

### Naming Conventions
- **Migration directories**: `m<sequential-number>_<snake_case_description>/` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Entity files**: Snake case singular noun (e.g., `advisory.rs`, `sbom.rs`, `package.rs`)
- **Module files**: `mod.rs` for module entry points

### Code Organization
- **Entity separation**: Database entities are defined in `entity/src/`, separate from migration code
- **Module registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Endpoint structure**: Routes under `/api/v2/<resource>` with separate files for `list.rs`, `get.rs`, etc.

## Test Conventions (from `tests/api/` siblings)

### Test File Structure
- **Location**: Integration tests in `tests/api/` directory, organized by domain (e.g., `advisory.rs`, `sbom.rs`, `search.rs`)
- **Database**: Tests hit a real PostgreSQL test database (integration tests, not unit tests with mocks)

### Assertion Patterns
- **Status codes**: Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for HTTP response validation
- **Response validation**: Deserialize response bodies and check specific field values

### Test Naming
- **Convention**: Test functions named descriptively matching the endpoint and scenario being tested

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` file at the root. This file should be read during implementation to extract any CI check commands and additional project-specific conventions not captured in the repository structure documentation.
