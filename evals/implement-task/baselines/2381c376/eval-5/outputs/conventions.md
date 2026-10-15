# Conventions Discovered from Sibling Analysis

## Source

Conventions derived from analyzing sibling files in the `migration/src/` directory, primarily `m0001_initial/mod.rs`, and from the repository's key conventions documented in repo-backend.md and CONVENTIONS.md.

## Migration Module Conventions

### File and Directory Naming
- Each migration lives in its own subdirectory under `migration/src/`
- Directory naming pattern: `m<NNNN>_<snake_case_description>/` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- Each migration directory contains a single `mod.rs` file

### Struct and Trait Pattern
- Each migration module defines a `pub struct Migration;`
- Implements `MigrationTrait` with two required methods: `up` and `down`
- Both methods are async and return `Result<(), DbErr>`
- Methods receive `&self` and `manager: &SchemaManager` as parameters

### Migration Registration
- All migrations are registered in `migration/src/lib.rs`
- Registered by adding `Box::new(<module>::Migration)` to the `vec![]` returned by the `migrations()` function
- Modules are declared at the top of `lib.rs` with `mod <module_name>;`
- Migrations are listed in sequential order

### SeaORM API Usage
- Table alterations use `Table::alter().table(<Entity>::Table)` builder pattern
- Column definitions use `ColumnDef::new(<Entity>::<Column>)` with chained type and constraint methods
- Entity column enums (e.g., `Advisory::Table`, `Advisory::Status`) reference SeaORM entity definitions from the `entity` crate
- All schema operations are awaited: `manager.<operation>.await`
- Operations end with `.to_owned()` before passing to the manager

## General Code Conventions (from repo-backend.md)

### Framework
- Axum for HTTP, SeaORM for database ORM
- Each domain module follows `model/ + service/ + endpoints/` structure

### Error Handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- Migrations return `Result<(), DbErr>`

### Import Organization
- SeaORM prelude imports for entity types
- Standard Rust module structure with `mod` declarations

### Testing
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`
- Migration tests verify both `up` and `down` methods execute successfully

### Documentation
- Every new public struct, trait implementation, and function should have a documentation comment using `///` (Rust doc comment convention)
- Per skill guidance, this applies regardless of whether sibling migrations have doc comments

## Skill Guidance Overrides

The following skill-level guidance takes precedence over any conflicting sibling patterns:

- **Test documentation**: Every test function must have a `///` doc comment explaining what it verifies, even if existing tests lack them
- **Value-based assertions**: Prefer asserting on actual values over length-only checks
- **Given-when-then comments**: Non-trivial tests should include `// Given`, `// When`, `// Then` section comments
