# Convention Conformance Analysis: TC-9205

## Sibling Analysis

Analyzed sibling migration `migration/src/m0001_initial/mod.rs` and related files.

### Migration Structure Conventions

1. **Module pattern**: Each migration lives in its own directory under `migration/src/` as `m<number>_<name>/mod.rs`
2. **Trait implementation**: Implements `MigrationTrait` with two async methods:
   - `up(&self, manager: &SchemaManager) -> Result<(), DbErr>` — applies the migration
   - `down(&self, manager: &SchemaManager) -> Result<(), DbErr>` — reverts the migration
3. **Registration**: Migrations are registered in `migration/src/lib.rs` in a `vec![]` inside the `migrations()` function, in chronological order
4. **SeaORM DDL**: Uses SeaORM's schema manager for all DDL operations (`TableAlterStatement`, `TableCreateStatement`, etc.)

### Error Handling Conventions

- Migration methods return `Result<(), DbErr>` (SeaORM's database error type)
- Service methods return `Result<T, AppError>` with `.context()` wrapping from `anyhow`
- Handlers propagate errors via `?` operator

### Entity Conventions

- Entities defined in `entity/src/` using SeaORM derive macros
- Each entity maps to a database table
- Column names defined as enum variants (e.g., `Advisory::Status`, `Advisory::Severity`)

### Test Conventions

- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`
- Test naming follows `test_<action>_<subject>` pattern

### Module Organization

- Domain modules follow `model/ + service/ + endpoints/` structure
- Each module's `endpoints/mod.rs` registers routes
- `server/main.rs` mounts all module routes

### No Conflicts Detected

No conflicts found between sibling conventions and the skill's built-in quality guidance for this task. The migration task is primarily structural (DDL), and the sibling patterns directly apply.
