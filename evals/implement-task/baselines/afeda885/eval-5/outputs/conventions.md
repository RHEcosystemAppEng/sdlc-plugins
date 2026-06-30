# Conventions Discovered from Sibling Analysis

## Source: Repository Structure and Key Conventions (repo-backend.md)

### Production Code Conventions

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders

### Migration Conventions (from `m0001_initial/mod.rs` sibling analysis)

- **Migration naming**: Migrations follow the `m<NNNN>_<snake_case_description>` pattern (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Module structure**: Each migration lives in its own directory under `migration/src/` with a `mod.rs` file
- **Trait implementation**: Migrations implement `MigrationTrait` from SeaORM with `up` and `down` methods
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding to the `vec![]` in the `migrations()` function
- **Table operations**: Use SeaORM's `TableAlterStatement` / `TableCreateStatement` API for schema changes
- **Rollback support**: Every `up` operation must have a corresponding `down` that reverses the change

### Entity Conventions (from `entity/src/advisory.rs` sibling analysis)

- **Entity files**: Each entity has its own file under `entity/src/` (e.g., `advisory.rs`, `sbom.rs`, `package.rs`)
- **SeaORM entities**: Entities are defined using SeaORM's derive macros and enum-based column definitions
- **Column naming**: Columns are defined as enum variants on the entity (e.g., `Advisory::Status`, `Advisory::Severity`)

### Test Conventions (from `tests/api/` sibling analysis)

- **Test location**: Integration tests live in `tests/api/` organized by domain (e.g., `advisory.rs`, `sbom.rs`)
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test database**: Integration tests hit a real PostgreSQL test database
- **Test naming**: Tests follow the `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Documentation Conventions

- **CONVENTIONS.md**: Present at repository root -- would be read for CI check commands and project-specific rules
- **README.md**: Present at repository root

### Naming Conventions

- **Service methods**: Follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_sboms`)
- **File naming**: Snake case throughout (Rust convention)
- **Module structure**: `mod.rs` as module entry point within each directory

### Import Organization

- Standard library imports first, then external crates, then internal modules (Rust convention)
