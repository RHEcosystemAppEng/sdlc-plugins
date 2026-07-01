# Conventions Discovered from Sibling Analysis

## Source: `migration/src/m0001_initial/mod.rs` (sibling migration)

### Migration Module Conventions

- **Module structure:** Each migration lives in its own subdirectory under `migration/src/` named with a sequential prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Entry point:** Each migration module has a `mod.rs` file as its entry point
- **Struct naming:** All migrations define a unit struct named `Migration` with `#[derive(DeriveMigrationName)]`
- **Trait implementation:** All migrations implement `MigrationTrait` with both `up` and `down` methods
- **Async trait:** Uses `#[async_trait::async_trait]` attribute on the trait implementation
- **Return type:** Both `up` and `down` return `Result<(), DbErr>`
- **Schema manager:** Both methods receive `&SchemaManager` for executing schema changes

### Registration Conventions (from `migration/src/lib.rs`)

- **Module declaration:** Each migration module is declared with `mod <module_name>;` at the top of `lib.rs`
- **Registration pattern:** Migrations are registered in a `migrations()` function that returns `Vec<Box<dyn MigrationTrait>>`
- **Ordering:** Migrations appear in sequential order in the vec (they execute in registration order)
- **Boxing:** Each migration is wrapped as `Box::new(<module>::Migration)`

### SeaORM Conventions

- **Table/column references:** Use `#[derive(Iden)]` enum for type-safe table and column name references
- **Enum naming:** The enum is named after the entity (e.g., `Advisory`) with variants for `Table` and column names (e.g., `Status`)
- **Schema API:** Use SeaORM's `Table::alter()` builder for DDL operations, chaining `.table()`, `.drop_column()` / `.add_column()`, and `.to_owned()`

## Source: Repository Key Conventions (from repo-backend.md)

### General Code Conventions

- **Framework:** Axum for HTTP, SeaORM for database
- **Module pattern:** Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

## Source: `tests/api/advisory.rs` (sibling test file)

### Test Conventions (inferred from project structure)

- **Test location:** Integration tests live in `tests/api/` and test against a real PostgreSQL test database
- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` naming pattern
- **Test scope for migrations:** Migration tests should verify:
  - Migration runs successfully (up)
  - Rollback works correctly (down re-adds column)
  - Existing queries continue to function after schema change

## CONVENTIONS.md

A `CONVENTIONS.md` file exists at the repository root. Its contents should be read during implementation (Step 4) to extract any CI check commands and additional coding standards not captured in the repo structure documentation.
