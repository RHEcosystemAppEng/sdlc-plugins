# Convention Conformance Analysis for TC-9205

## Sibling analysis

Analyzed sibling files to understand established conventions in the trustify-backend repository.

### Migration conventions (from `migration/src/m0001_initial/mod.rs`)

1. **Migration struct pattern**: Each migration module defines a `pub struct Migration` with `#[derive(DeriveMigrationName)]`
2. **Trait implementation**: Implements `MigrationTrait` with both `up` and `down` async methods
3. **Error handling**: Methods return `Result<(), DbErr>` -- SeaORM's standard migration error type
4. **Async trait**: Uses `#[async_trait::async_trait]` attribute for async trait implementation
5. **Iden enums**: Table and column identifiers defined using `#[derive(Iden)] enum` for type-safe SQL generation
6. **Module naming**: Migration directories use numbered prefix format: `m0001_`, `m0002_`, etc.
7. **Registration**: Migrations are registered in `migration/src/lib.rs` in the `migrations()` function using `Box::new(ModuleName::Migration)`

### Entity conventions (from `entity/src/advisory.rs`)

1. **SeaORM entity pattern**: Entities use `#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]` with `#[sea_orm(table_name = "...")]`
2. **Column definitions**: Each column maps to a Rust type with SeaORM attributes
3. **Relationship definitions**: Uses `impl RelationTrait` and `impl Related<T>` for entity relationships

### Module structure conventions (from repository tree)

1. **Domain module pattern**: Each domain follows `model/ + service/ + endpoints/` three-tier structure
2. **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`
3. **Response types**: List endpoints use `PaginatedResults<T>` from `common/src/model/paginated.rs`
4. **Route registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules

### Test conventions (from `tests/api/`)

1. **Integration test style**: Tests hit a real PostgreSQL test database
2. **Assertion pattern**: `assert_eq!(resp.status(), StatusCode::OK)` for status checks
3. **Test file organization**: One test file per domain module (e.g., `tests/api/advisory.rs`, `tests/api/sbom.rs`)

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` file at the root. If accessible, it would be read for CI check commands and code generation commands. These would be executed during Step 9's CI checks verification.

## Conflicts detected

None. The migration conventions from the sibling `m0001_initial` are consistent with the task's Implementation Notes and the skill's quality guidance.
