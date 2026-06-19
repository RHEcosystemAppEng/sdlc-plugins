# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Migration structure (from `migration/src/m0001_initial/mod.rs`)

- **Trait implementation:** All migrations implement `MigrationTrait` with `up` and `down` methods
- **Module pattern:** Each migration lives in its own directory under `migration/src/` named `m<NNNN>_<description>/mod.rs`
- **Naming convention:** Migration directories follow sequential numbering: `m0001_`, `m0002_`, etc.
- **Column operations:** Use SeaORM's `TableAlterStatement` for column modifications (e.g., `Table::alter().table(...).drop_column(...).to_owned()`)
- **Manager usage:** Both `up` and `down` methods receive a `&SchemaManager` and use `manager.alter_table(...)` or equivalent

### Migration registration (from `migration/src/lib.rs`)

- **Registration pattern:** Migrations are registered in a `vec![]` inside the `migrations()` function
- **Module declaration:** Each migration module is declared with `mod m<NNNN>_<description>;`
- **Ordering:** Migrations appear in sequential order in the vec

### Framework conventions (from repo-wide patterns)

- **Framework:** Axum for HTTP, SeaORM for database ORM
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Module structure:** Each domain module follows `model/ + service/ + endpoints/` pattern
- **Endpoint registration:** Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Entity pattern:** SeaORM entities in `entity/src/` with one file per table

## Test Conventions

### Integration test patterns (from `tests/api/advisory.rs` and siblings)

- **Assertion style:** Use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation:** List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases:** Endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Database:** Integration tests hit a real PostgreSQL test database
- **Test runner:** `cargo test`

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` at the root. Its contents should be read during implementation for any CI check commands and additional project-specific conventions. Verification commands extracted from it would be run during Step 9's CI checks sub-step.
