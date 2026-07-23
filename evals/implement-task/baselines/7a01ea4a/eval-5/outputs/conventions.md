# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Migration pattern (from `migration/src/m0001_initial/mod.rs`)

- **Struct**: Each migration defines a unit struct `Migration` with `#[derive(DeriveMigrationName)]`
- **Trait implementation**: Implements `MigrationTrait` via `#[async_trait::async_trait]`
- **Method signatures**: `up` and `down` methods take `&self` and `&SchemaManager`, return `Result<(), DbErr>`
- **Builder pattern**: SeaORM table operations use method chaining with `.to_owned()` to finalize
- **Local Iden enums**: Migrations define local `#[derive(Iden)]` enums for table/column identifiers rather than importing from the entity crate, ensuring migration self-containment
- **Module naming**: Migration modules follow `m<sequential-number>_<descriptive_snake_case>` pattern (e.g., `m0001_initial`)

### Migration registration (from `migration/src/lib.rs`)

- **Module declarations**: Each migration module is declared with `mod m<number>_<name>;`
- **Registration**: Migrations are registered in a `vec![]` inside the `migrations()` function using `Box::new(module::Migration)` syntax
- **Ordering**: Migrations are listed in sequential order; execution order follows the vec order

### Entity pattern (from `entity/src/advisory.rs` and siblings)

- **Framework**: SeaORM entities with derive macros
- **Module registration**: Entity modules declared in `entity/src/lib.rs`
- **Column mapping**: Each column maps to an enum variant in the entity's `Column` enum

### Error handling (from `common/src/error.rs` and module endpoints)

- **Return type**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Error enum**: Centralized `AppError` enum that implements `IntoResponse`

### Module structure (from `modules/fundamental/src/advisory/`)

- **Domain pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes
- **Response types**: List endpoints return `PaginatedResults<T>`

### Naming conventions

- **Service methods**: Follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_advisories`)
- **File naming**: Snake case matching the domain entity name (e.g., `advisory.rs`, `sbom.rs`)

## Test Conventions

### Integration tests (from `tests/api/advisory.rs` and siblings)

- **Location**: Integration tests in `tests/api/` directory, one file per domain entity
- **Database**: Tests hit a real PostgreSQL test database
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code checks
- **Response validation**: Deserialize response body and check specific field values
- **Naming**: Test functions follow `test_<endpoint>_<scenario>` pattern

## Framework and Tooling

- **HTTP framework**: Axum
- **ORM**: SeaORM
- **Caching**: tower-http caching middleware
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
