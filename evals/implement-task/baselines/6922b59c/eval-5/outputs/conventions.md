# Conventions Discovered from Sibling Analysis

Conventions identified by analyzing sibling files in the trustify-backend repository, organized by category. These serve as binding references during implementation.

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

### File and Module Naming
- Migration modules follow the pattern `m<NNNN>_<snake_case_description>/mod.rs`
- Numbering is zero-padded to 4 digits (e.g., `m0001`, `m0002`)
- Each migration lives in its own directory under `migration/src/`

### Struct and Type Naming
- Migration struct is always named `Migration` (each module has its own)
- Uses `#[derive(DeriveMigrationName)]` to auto-derive the migration name from the module path
- Local `#[derive(Iden)]` enums define table and column identifiers scoped to the migration

### Code Structure Pattern
- Import: `use sea_orm_migration::prelude::*;`
- Struct definition with `DeriveMigrationName` derive
- `#[async_trait::async_trait]` on the `MigrationTrait` impl block
- Both `up()` and `down()` methods implemented for reversibility
- Return type: `Result<(), DbErr>`

### Error Handling
- Migrations propagate errors via `?` operator and `Result<(), DbErr>` return type
- No explicit error wrapping -- SeaORM's `DbErr` is used directly

## Registration Conventions (from `migration/src/lib.rs`)

### Module Registration
- Each migration module is declared with `mod m<NNNN>_<name>;` in `lib.rs`
- Modules are listed in numerical order
- Migrations are registered in a `migrations()` function returning `Vec<Box<dyn MigrationTrait>>`
- Registration uses `Box::new(<module>::Migration)` pattern
- Order in the vec determines execution order

## Entity Conventions (from `entity/src/advisory.rs`)

### SeaORM Entity Pattern
- Entities use SeaORM's `DeriveEntityModel` derive macro
- Column identifiers are defined as enum variants
- The `advisory` entity no longer includes a `Status` variant (confirmed removed in prior migration)

## General Rust Conventions (from repo structure)

### Framework Stack
- HTTP: Axum
- ORM: SeaORM
- Database: PostgreSQL
- Async runtime: Tokio

### Module Organization
- Domain modules follow `model/ + service/ + endpoints/` structure
- Error handling uses `Result<T, AppError>` with `.context()` wrapping in handlers
- List endpoints return `PaginatedResults<T>`

## Test Conventions (from `tests/api/`)

### Test Infrastructure
- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Test files named after the domain entity (e.g., `advisory.rs`, `sbom.rs`)

### Assertion Patterns
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`
- Value-based assertions preferred over length-only checks (per skill guidance override)

### Test Naming
- Function names follow `test_<what_is_being_tested>` pattern

## Skill Guidance Overrides

The following skill-mandated conventions override sibling patterns where they conflict:

1. **Documentation comments on all new symbols** -- every struct, enum, and public function gets a doc comment, even if sibling code lacks them
2. **Value-based assertions** -- assert on actual values, not just counts, even if sibling tests use `.len()` checks
3. **Given-when-then comments** -- non-trivial test bodies include `// Given`, `// When`, `// Then` section markers
4. **Test function documentation** -- every test function gets a doc comment explaining what it verifies
