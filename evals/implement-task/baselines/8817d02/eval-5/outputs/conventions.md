# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)
- **Trait implementation:** Each migration module implements `MigrationTrait` with `up` and `down` async methods
- **Module structure:** Each migration lives in its own directory under `migration/src/` as `m<NNNN>_<name>/mod.rs`
- **Naming convention:** Migration directories follow the pattern `m<sequential-number>_<snake_case_description>` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Schema operations:** Migrations use SeaORM's schema builder API (`Table::alter()`, `Table::create()`, etc.) rather than raw SQL
- **Rollback support:** Every `up` migration has a corresponding `down` method that reverses the change for rollback capability

### Migration Registration (from `migration/src/lib.rs`)
- **Registration pattern:** All migrations are registered in a `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>`
- **Ordering:** Migrations are listed in sequential order in the `vec![]` macro
- **Module declaration:** Each migration module is declared with `mod m<NNNN>_<name>;` at the top of `lib.rs`

### Entity Pattern (from `entity/src/advisory.rs`)
- **ORM framework:** SeaORM entities define table structure with derive macros
- **Column enum:** Each entity has a `Column` enum variant for every database column
- **Table enum:** Entities define a `Table` enum for table-level operations

### General Codebase Conventions
- **Framework:** Axum for HTTP, SeaORM for database
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Module pattern:** Each domain module follows `model/ + service/ + endpoints/` structure
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

## Test Conventions

### Integration Tests (from `tests/api/advisory.rs` and siblings)
- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern followed by body deserialization
- **Test database:** Integration tests hit a real PostgreSQL test database
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Test location:** Integration tests live in `tests/api/` directory, organized by entity
