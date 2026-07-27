# Conventions Discovered from Sibling Analysis

## Source of Analysis

Conventions were discovered by inspecting sibling files in the trustify-backend repository, specifically:
- `migration/src/m0001_initial/mod.rs` (sibling migration)
- `entity/src/advisory.rs` (related entity)
- `migration/src/lib.rs` (migration registry)
- Repository-level conventions from `Key Conventions` in the repo structure documentation

## Production Code Conventions

### Migration Pattern
- Each migration lives in its own subdirectory under `migration/src/` named with a sequential prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- Each migration module contains a single `mod.rs` file
- Migrations define a `Migration` struct with `#[derive(DeriveMigrationName)]`
- Migrations implement `MigrationTrait` with async `up` and `down` methods
- Both `up` and `down` must be implemented to support rollback
- Uses `sea_orm_migration::prelude::*` for imports

### Entity Pattern
- SeaORM entities are defined in `entity/src/` with one file per table
- Entity files use `DeriveIden` enums for table and column identifiers
- The advisory entity uses a `severity` field (enum) that replaced the old `status` column

### Module Registration
- Migrations are registered in `migration/src/lib.rs` via `mod` declarations and a `migrations()` function
- The `migrations()` function returns `Vec<Box<dyn MigrationTrait>>`
- Migrations are listed in sequential order in the vec

### Framework Conventions
- **Framework**: Axum for HTTP, SeaORM for database
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure

### Naming Conventions
- Migration directories use snake_case with numeric prefix: `m{NNNN}_{description}`
- Migration structs are always named `Migration` (the module path provides uniqueness)
- Column identifiers use PascalCase enum variants (e.g., `Advisory::Status`, `Advisory::Table`)

## Test Conventions

### Test Structure
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Test files are named after the domain they test (e.g., `advisory.rs`, `sbom.rs`)
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization

### Migration Testing
- Migration tests should verify both `up` (forward) and `down` (rollback) paths
- Tests run against a real PostgreSQL test database
- After migration runs, verify that queries against the affected table still work correctly

## Documentation Conventions
- Repository has a `CONVENTIONS.md` at the root (should be read for CI check commands)
- Each crate has its own `Cargo.toml`
