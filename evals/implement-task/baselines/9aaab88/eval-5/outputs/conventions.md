# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)

- **Structure**: Each migration is a separate module under `migration/src/` in its own directory (e.g., `m0001_initial/mod.rs`), containing a `Migration` struct that implements `MigrationName` and `MigrationTrait`.
- **Naming**: Migration directories follow the pattern `m<NNNN>_<descriptive_name>` with zero-padded sequential numbering.
- **MigrationName**: Returns the directory name as a string (e.g., `"m0001_initial"`).
- **MigrationTrait**: Implements `up` (apply) and `down` (rollback) async methods. Both return `Result<(), DbErr>`.
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding `Box::new(<module>::Migration)` to the `vec![]` returned by the `migrations()` function. Order in the vec determines execution order.
- **Column identifiers**: Migrations define local `Iden` enums for table and column references rather than importing from entity crate, since the entity may have already changed (e.g., the column being dropped is no longer in the entity).
- **Framework**: SeaORM migration framework (`sea_orm_migration::prelude::*`).

### Module Structure (from `modules/fundamental/src/`)

- **Domain modules**: Follow `model/ + service/ + endpoints/` structure.
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`).
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`).
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### Entity Conventions (from `entity/src/`)

- **SeaORM entities**: Each entity is a separate file in `entity/src/` (e.g., `advisory.rs`, `sbom.rs`).
- **Column enum**: Each entity defines a column enum with `#[derive(Iden)]` for type-safe column references in queries and migrations.

## Test Conventions (from `tests/api/`)

- **Location**: Integration tests reside in `tests/api/` with one file per domain (e.g., `advisory.rs`, `sbom.rs`).
- **Database**: Tests run against a real PostgreSQL test database (not mocked).
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization and field assertions.
- **Naming**: Test functions follow `test_<entity>_<action>_<scenario>` pattern.

## Framework and Tooling

- **HTTP framework**: Axum
- **ORM**: SeaORM
- **Build**: Cargo (Rust)
- **Testing**: `cargo test`
