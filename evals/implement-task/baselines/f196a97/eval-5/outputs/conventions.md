# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Migration Module Structure
- Each migration lives in its own directory under `migration/src/`, named with a sequential prefix and descriptive name (e.g., `m0001_initial/`, `m0002_drop_advisory_status/`)
- Each migration directory contains a single `mod.rs` file
- Migrations implement the `MigrationTrait` trait from SeaORM

### Migration Implementation Pattern (from `m0001_initial/mod.rs`)
- **Trait**: implement `MigrationTrait` with `up` and `down` async methods
- **Method signatures**: `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` and `async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr>`
- **Table operations**: use SeaORM's schema manager API (`manager.alter_table(...)`, `manager.create_table(...)`, etc.)
- **Column definitions**: use `ColumnDef::new(...)` for column specifications
- **Return type**: `Result<(), DbErr>` with `.await` on schema operations

### Migration Registration Pattern (from `migration/src/lib.rs`)
- Migrations are registered in a `migrations()` function that returns `Vec<Box<dyn MigrationTrait>>`
- Each migration is added as `Box::new(m0001_initial::Migration)` (or equivalent) to the `vec![]`
- Module declarations use `mod m0001_initial;` at the top of `lib.rs`

### Error Handling
- All handlers and services return `Result<T, AppError>` with `.context()` for error wrapping
- Migrations use `Result<(), DbErr>` (SeaORM's error type)

### Naming Conventions
- **Migration directories**: `m<NNNN>_<snake_case_description>/` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Migration struct**: `Migration` (simple name, scoped by module)
- **Service methods**: `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_sboms`)
- **Entity columns**: snake_case enum variants mapping to database column names

### Module and File Organization
- Domain modules follow `model/ + service/ + endpoints/` structure
- Entity definitions in `entity/src/` as individual files per entity
- Shared utilities in `common/src/`

### Framework Conventions
- **HTTP**: Axum for HTTP routing and handlers
- **ORM**: SeaORM for database operations
- **Response types**: list endpoints return `PaginatedResults<T>`
- **Query helpers**: shared filtering, pagination, sorting via `common/src/db/query.rs`

## Test Conventions

### Test Structure (from `tests/api/advisory.rs` and siblings)
- **Location**: integration tests in `tests/api/` directory, one file per domain entity
- **Database**: tests use a real PostgreSQL test database
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks, followed by body deserialization
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Response Validation Pattern
- List endpoint tests validate `total_count`, `items.len()`, and key fields on at least one item
- Error case tests include 404 checks with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Documentation
- Every test function should have a `///` doc comment explaining what it verifies (per skill requirement, overriding existing convention if siblings lack doc comments)
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments
