# Conventions Discovered from Sibling Analysis

Conventions extracted during Step 4 (Understand the Code) by analyzing sibling files
in the trustify-backend repository, organized by category.

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

### Structure
- Each migration lives in its own module directory: `migration/src/m<NNNN>_<snake_case_name>/mod.rs`
- Module naming follows sequential numbering: `m0001_`, `m0002_`, etc.
- Each module exports a `pub struct Migration;` unit struct

### Imports
- Single wildcard import: `use sea_orm_migration::prelude::*;`
- No other external crate imports in migration files

### Trait Implementation
- Derive migration name from module path: `#[derive(DeriveMigrationName)]`
- Implement `MigrationTrait` with `#[async_trait::async_trait]` attribute
- Two required methods: `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>`
  and `async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr>`

### Table/Column Identifiers
- Declare a local `#[derive(Iden)] enum` for table and column names within each migration
- Do NOT import from the entity crate — migrations must be self-contained and stable
  regardless of entity changes

### Registration
- Migrations registered in `migration/src/lib.rs` via `mod <module_name>;` declaration
  and `Box::new(<module_name>::Migration)` entry in the `migrations()` vec
- Order in the vec determines execution order — must be chronological

## Error Handling Conventions (from service and endpoint files)

- Service and endpoint functions return `Result<T, AppError>` with `.context()` wrapping
- Migration functions return `Result<(), DbErr>` directly (no `.context()` wrapping)

## Naming Conventions

- **Files**: `snake_case` for all Rust files
- **Modules**: `snake_case` directory and module names
- **Structs**: `PascalCase` (e.g., `Migration`, `AdvisorySummary`, `SbomDetails`)
- **Functions**: `snake_case` (e.g., `migrations()`, `up()`, `down()`)
- **Enums**: `PascalCase` with `PascalCase` variants (e.g., `Advisory::Table`, `Advisory::Status`)

## Test Conventions (from `tests/api/`)

- Integration tests live in `tests/api/<entity>.rs`
- Tests use real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` — value-based assertions
- Async tests use `#[tokio::test]`

## Module Organization Conventions

- Domain modules follow `model/ + service/ + endpoints/` structure
- Each domain module has its own `mod.rs` for re-exports
- Entity definitions live in the `entity/` crate, separate from service logic

## Code Quality Conventions

- Public structs and functions have documentation comments
- Defensive null/option handling via Rust's type system (`Option<T>`, `.unwrap_or_default()`)

## Potential Convention Conflicts

None detected. The task description aligns with all discovered conventions.

## Skill Guidance vs. Sibling Patterns

- **Test documentation**: Sibling tests in `tests/api/` may not have doc comments on every
  test function. Per skill guidance (Step 7), doc comments are added to every test function
  regardless — this overrides the sibling pattern.
- **Given/When/Then comments**: Sibling tests may not use section comments. Per skill
  guidance, non-trivial tests include `// Given`, `// When`, `// Then` comments.
