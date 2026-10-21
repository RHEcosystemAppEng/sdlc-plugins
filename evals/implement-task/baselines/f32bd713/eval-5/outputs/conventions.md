# Conventions Discovered from Sibling Analysis

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

- **Module structure**: Each migration lives in its own directory under `migration/src/` following the naming pattern `m<NNNN>_<snake_case_description>/mod.rs`
- **Trait implementation**: Every migration module implements `MigrationTrait` with two required methods: `up` (apply) and `down` (rollback)
- **SeaORM API**: Migrations use SeaORM's schema management API (`SchemaManager`, `TableAlterStatement`, `Table::alter()`, `ColumnDef`)
- **Return type**: Both `up` and `down` return `Result<(), DbErr>` using `async_trait`
- **Entity references**: Migrations reference entity enums (e.g., `Advisory::Table`, `Advisory::Status`) for type-safe table/column names
- **Registration**: Migrations are registered in `migration/src/lib.rs` inside the `migrations()` function by adding `Box::new(m<NNNN>_<name>::Migration)` to the `vec![]`

## Entity Conventions (from `entity/src/advisory.rs` and siblings)

- **SeaORM derive macros**: Entities use `#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]` and related SeaORM macros
- **Column enum**: Each entity defines a `Column` enum with variants mapping to database column names
- **Table naming**: The `#[sea_orm(table_name = "...")]` attribute specifies the database table

## Error Handling

- **Result types**: Functions return `Result<T, DbErr>` for database operations
- **Context wrapping**: Service-layer code uses `.context()` for error enrichment (from `AppError`)

## Naming Conventions

- **Files**: snake_case for all Rust files
- **Modules**: snake_case directory names with `mod.rs` inside
- **Migration directories**: `m<sequence_number>_<descriptive_name>/`
- **Functions/methods**: snake_case (`up`, `down`)
- **Types/Structs**: PascalCase (`Migration`, `Advisory`)

## Import Organization

- Standard library imports first, then external crates (sea_orm_migration, etc.), then local modules

## Test Conventions

- **Location**: Integration tests in `tests/api/` directory
- **Pattern**: Tests hit a real PostgreSQL test database
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Framework**: Standard Rust `#[test]` or `#[tokio::test]` for async tests
