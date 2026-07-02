# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Migration pattern (from `migration/src/m0001_initial/mod.rs`)
- Each migration lives in its own directory under `migration/src/` named `m<NNNN>_<description>/`
- Each migration module contains a `mod.rs` with a public `Migration` struct
- Migrations implement `MigrationName` (returning the module name) and `MigrationTrait` (with `up` and `down` methods)
- `async_trait::async_trait` attribute is used on the `MigrationTrait` impl
- Table and column identifiers use a locally-defined `#[derive(Iden)] enum` rather than importing from entity crates, making migrations self-contained and independent of current entity state

### Migration registration (from `migration/src/lib.rs`)
- Each migration module is declared with `mod <module_name>;`
- Migrations are registered in a `migrations()` function that returns `Vec<Box<dyn MigrationTrait>>`
- Migrations are listed in chronological order inside a `vec![]` macro

### Error handling (from modules throughout the codebase)
- All handlers return `Result<T, AppError>` with `.context()` for error wrapping
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`

### Naming conventions
- Migration directories: `m<NNNN>_<snake_case_description>/`
- Service methods: `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `fetch`, `list`)
- Module structure: each domain follows `model/ + service/ + endpoints/` structure

### Entity pattern (from `entity/src/advisory.rs` and siblings)
- SeaORM entities with `DeriveEntityModel` derive macro
- Each entity in its own file under `entity/src/`
- Column definitions map to database columns

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Shared filtering, pagination, and sorting via `common/src/db/query.rs`

## Test Conventions

### Integration tests (from `tests/api/advisory.rs` and siblings)
- Integration tests live in `tests/api/` and test against a real PostgreSQL test database
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Test naming follows `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- Tests validate response structure including `total_count`, `items.len()`, and key fields of individual items
- Error cases include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Migration tests
- Migration tests verify both `up` and `down` operations
- Tests run against a test database to confirm schema changes apply and rollback correctly
- Queries are executed after migration to verify existing data access patterns still work
