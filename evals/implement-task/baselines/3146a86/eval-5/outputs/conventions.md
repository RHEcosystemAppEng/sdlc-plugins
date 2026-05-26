# Discovered Conventions

## Source: CONVENTIONS.md at repository root

The repository contains a `CONVENTIONS.md` file at `trustify-backend/CONVENTIONS.md`.
Contents should be read in full to extract CI check commands and code conventions.
Based on the repository structure described in repo-backend.md, the following conventions
were identified from sibling analysis.

---

## Conventions from Sibling Analysis

### Sibling files inspected

For `migration/src/m0002_drop_advisory_status/mod.rs` (file to create):
- Sibling: `migration/src/m0001_initial/mod.rs` — the only existing migration module;
  serves as the canonical pattern reference.

For `migration/src/lib.rs` (file to modify):
- Only file in its location; the migration list registration pattern is inferred from
  the task's Implementation Notes and `m0001_initial` usage.

For `entity/src/advisory.rs` (inspected to verify `status` column absence):
- Siblings: `entity/src/sbom.rs`, `entity/src/package.rs` — other SeaORM entity files.

---

## Discovered Conventions (Production Code)

### Framework & ORM
- **HTTP framework**: Axum for HTTP routing; all handlers return `Result<T, AppError>`
- **ORM**: SeaORM for all database access; entities follow SeaORM's `EntityTrait` pattern
- **Migration trait**: Migrations implement `MigrationTrait` with `up` and `down` async methods
- **Schema alteration**: DDL changes use SeaORM's `SchemaManager` + `TableAlterStatement` / `TableCreateStatement`

### Migration module structure (from `m0001_initial/mod.rs` pattern)
- Each migration lives in its own directory under `migration/src/`, named `m<NNNN>_<description>/`
- The directory contains a single `mod.rs`
- The module declares a `pub struct Migration` (unit struct)
- `impl MigrationName for Migration` returns the module name as a string constant
- `impl MigrationTrait for Migration` provides:
  - `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` — applies the schema change
  - `async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr>` — reverts the schema change
- Both `up` and `down` must be present to allow rollback

### Migration registration (`migration/src/lib.rs`)
- A `migrations()` function returns `Vec<Box<dyn MigrationTrait>>`
- Each migration is added to the `vec![]` as `Box::new(<Module>::Migration)`
- Modules are declared as `mod m0001_initial;` at the top of `lib.rs`
- New migrations are appended after the last existing entry

### Entity conventions (`entity/src/advisory.rs` and siblings)
- SeaORM entities use the `DeriveEntityModel` derive macro
- Column enums are named `Column` and implement `ColumnTrait`
- Table enum variants match the database table name in snake_case
- Column variant names use PascalCase (e.g., `Advisory::Status`, `Advisory::Severity`)
- Nullable columns are declared with `.null()` in `ColumnDef`

### Error handling
- All async database functions return `Result<(), DbErr>` in migrations
- Handlers in service/endpoint code return `Result<T, AppError>` with `.context()` wrapping

### Naming conventions
- Migration directories: `m<NNNN>_<snake_case_description>` (zero-padded 4-digit index)
- Migration structs: `Migration` (consistent across all migration modules)
- Service methods: `verb_noun` pattern (e.g., `get_advisory`, `list_sboms`)
- Module files: `mod.rs` as the entry point within each directory

### Import organization
- SeaORM imports: `use sea_orm_migration::prelude::*;`
- Entity references in migrations use the entity crate, e.g., `use entity::advisory::*;` or
  reference the table via a local enum matching the entity's `Iden` derive

### Documentation on new symbols
- Public structs and trait implementations should have a `///` doc comment
- One line is sufficient for simple types; functions with non-obvious behavior get a brief explanation

---

## Discovered Test Conventions

### Sibling test files inspected
- `tests/api/advisory.rs` — advisory endpoint integration tests
- `tests/api/sbom.rs` — SBOM endpoint integration tests

### Test patterns
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: list endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases**: 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<action>_<scenario>` (e.g., `test_migration_up_drops_status_column`)
- **Test setup**: integration tests hit a real PostgreSQL test database; fixtures seeded before assertions
- **Documentation**: each test function preceded by `///` doc comment explaining what it verifies
- **Structure**: non-trivial tests use `// Given`, `// When`, `// Then` comments
- **Migration tests**: verify column absence after `up`, column presence after `down`

### CI check commands (from CONVENTIONS.md)

The following commands should be run before committing (extracted from CONVENTIONS.md
CI checks section — exact commands depend on actual file content, listed here as
representative based on Rust project conventions):

```
cargo fmt --check
cargo clippy -- -D warnings
cargo build
cargo test
```
