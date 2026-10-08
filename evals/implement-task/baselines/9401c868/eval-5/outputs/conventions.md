# Conventions Discovered from Sibling Analysis

## Source

Sibling file analyzed: `migration/src/m0001_initial/mod.rs` -- the only existing migration module and direct pattern reference cited in the task's Implementation Notes.

Additional sources: repository structure conventions from `repo-backend.md`, project CLAUDE.md conventions.

## Discovered Conventions

### Migration Module Structure

- Each migration lives in its own subdirectory under `migration/src/` following the naming pattern `m<NNNN>_<snake_case_description>/mod.rs`
- Sequential numbering: m0001, m0002, m0003, etc.
- Module name matches the directory name

### Migration Implementation Pattern

- Define a public unit struct (e.g., `pub struct Migration;`)
- Implement `MigrationTrait` for the struct with three required methods:
  - `fn name(&self) -> &str` -- returns the migration name as a static string
  - `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- applies the migration
  - `async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- rolls back the migration
- Use SeaORM's schema manager and table alteration API
- Use entity enums (e.g., `Advisory::Table`, `Advisory::Status`) for type-safe table/column references

### Migration Registration Pattern

- All migrations are registered in `migration/src/lib.rs` in a `migrations()` function
- The function returns a `Vec<Box<dyn MigrationTrait>>` containing `Box::new(module::Migration)` entries
- New migrations are appended to the end of the vec (order matters)
- Each migration module is declared with `mod m0002_drop_advisory_status;` at the top of lib.rs

### Framework Conventions (from repo structure)

- **ORM**: SeaORM for database operations
- **Entities**: Defined in `entity/src/` with SeaORM derive macros
- **Error handling**: Functions return `Result<T, DbErr>` in migration context
- **Testing**: Integration tests in `tests/api/` use a real PostgreSQL test database
- **Test assertions**: `assert_eq!(resp.status(), StatusCode::OK)` pattern

### Naming Conventions

- Snake case for module names and function names (Rust standard)
- Migration directories: `m<sequence>_<descriptive_name>/`
- Struct names: PascalCase (e.g., `Migration`)

### Import Organization

- SeaORM imports at the top of migration files (`sea_orm_migration::prelude::*`)
- Entity imports for table/column enum references

### Error Handling

- Migration methods propagate errors via `?` operator
- Return type is `Result<(), DbErr>`
- No custom error wrapping in migration code (SeaORM handles error context)

### Test Conventions

- Integration tests hit a real PostgreSQL test database
- Test assertion pattern: `assert_eq!` for status codes and values
- Tests organized by domain in `tests/api/` directory

### Skill Guidance Overrides

- **Test documentation**: Every test function must have a `///` doc comment (skill standard, regardless of sibling practice)
- **Value-based assertions**: Assert on actual values, not just counts (skill standard takes precedence)
- **Given-when-then comments**: Non-trivial tests should include `// Given`, `// When`, `// Then` section comments
