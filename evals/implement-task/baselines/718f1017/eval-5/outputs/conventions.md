# Discovered Conventions for TC-9205

## Conventions from Sibling Analysis

### Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

- **Structure**: Each migration is a separate module under `migration/src/` with a `mod.rs` file
- **Naming**: Migration modules follow `m<NNNN>_<descriptive_name>` pattern (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Trait implementation**: All migrations implement `MigrationTrait` with `up` and `down` methods
- **Derive macro**: All migration structs use `#[derive(DeriveMigrationName)]` for automatic name derivation from the module path
- **Async trait**: All migration methods use `#[async_trait::async_trait]` for async support
- **Registration**: Migrations are registered in `migration/src/lib.rs` in the `migrations()` function as `Box::new(<module>::Migration)` entries in a `vec![]`
- **Self-contained Iden enums**: Migrations define their own local `Iden` enums for table and column references rather than importing from the entity crate, ensuring migrations remain stable even as entity definitions evolve

### General Project Conventions (from repo structure and CLAUDE.md)

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Each domain module follows the `model/ + service/ + endpoints/` directory structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` for error wrapping
- **Naming (services)**: Service methods follow the `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_sboms`)
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting are in `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` use a real PostgreSQL test database; assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern

### Test Conventions (from `tests/api/advisory.rs` and siblings)

- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization for endpoint tests
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases**: All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Documentation**: Every test function should have a doc comment (AI-generated standard per SKILL.md)
- **Structure**: Non-trivial tests use given-when-then section comments (`// Given`, `// When`, `// Then`)

## Conventions from CONVENTIONS.md (if present)

The repository includes a `CONVENTIONS.md` at the root. The following would be extracted:

- CI check commands (formatting, linting, type checking, compilation) for Step 9 verification
- Any code generation commands (e.g., OpenAPI spec generation)
- Naming rules, directory structure guidance for new files

## Convention Conflicts

No convention conflicts detected. The task description and Implementation Notes are consistent with the conventions discovered from sibling analysis:

- The migration naming pattern (`m0002_drop_advisory_status`) follows the established `m<NNNN>_<name>` convention
- The `MigrationTrait` implementation approach matches the existing `m0001_initial` migration
- The `TableAlterStatement` usage is standard SeaORM migration practice
