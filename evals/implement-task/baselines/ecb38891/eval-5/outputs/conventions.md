# Convention Conformance Analysis: TC-9205

## Sibling Analysis

Analyzed the following sibling files to identify established conventions:

### Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

1. **Migration struct pattern**: Each migration module defines a `Migration` struct with `#[derive(DeriveMigrationName)]` and implements `MigrationTrait` with `up` and `down` async methods.

2. **Module structure**: Each migration lives in its own directory as `migration/src/m<number>_<name>/mod.rs`.

3. **Registration pattern**: Migrations are registered in `migration/src/lib.rs` by adding `Box::new(module::Migration)` to the `vec![]` returned by the `migrations()` function.

4. **Error handling**: Migration methods return `Result<(), DbErr>` — SeaORM's database error type. No custom error wrapping is used in migrations.

5. **Table alteration API**: Uses SeaORM's `Table::alter()` fluent builder API with `manager.alter_table(...)` for schema changes.

### General Codebase Conventions (from repo-backend structure)

1. **Error handling**: Handlers use `Result<T, AppError>` with `.context()` wrapping for error messages (from `common/src/error.rs`).

2. **Module structure**: Each domain follows the `model/ + service/ + endpoints/` pattern within `modules/fundamental/src/`.

3. **Entity definitions**: SeaORM entities live in `entity/src/` with one file per table (e.g., `advisory.rs`, `sbom.rs`).

4. **Naming conventions**:
   - Migration directories: `m<number>_<descriptive_name>/`
   - Service files: `<domain>.rs` (e.g., `advisory.rs`, `sbom.rs`)
   - Endpoint files: verb-based (`list.rs`, `get.rs`)

5. **Testing conventions**: Integration tests in `tests/api/` using `assert_eq!(resp.status(), StatusCode::OK)` pattern. Tests hit a real PostgreSQL test database.

6. **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

7. **Query helpers**: Shared filtering, pagination, and sorting utilities in `common/src/db/query.rs`.

## Conventions Applied to This Task

For the migration implementation (TC-9205):
- Follow the `MigrationTrait` pattern from `m0001_initial/mod.rs`
- Use the `m<number>_<name>/mod.rs` directory convention
- Return `Result<(), DbErr>` from migration methods
- Use SeaORM's `Table::alter()` API for schema changes
- Register in `lib.rs` following the existing `Box::new()` pattern

## No Convention Conflicts Detected

No conflicts between task instructions, implementation notes, and discovered conventions. The task's implementation notes align with the patterns observed in sibling migration code.
