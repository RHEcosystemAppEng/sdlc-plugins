# Conventions Discovered from Sibling Analysis

## Source of Analysis

Sibling file analyzed: `migration/src/m0001_initial/mod.rs` -- the only existing migration module, serving as the canonical pattern for all new migrations.

Additional context from: `entity/src/advisory.rs`, `modules/fundamental/src/advisory/` module, and repository-level `CONVENTIONS.md`.

## Discovered Conventions (from sibling migration analysis)

### Migration Structure
- **Module layout**: Each migration lives in its own directory under `migration/src/` named `m<NNNN>_<descriptive_name>/mod.rs`
- **Numbering**: Migrations use zero-padded four-digit sequential numbers (m0001, m0002, ...)
- **Registration**: Each migration module is declared with `mod` in `migration/src/lib.rs` and added to the `migrations()` vec in chronological order

### Migration Implementation Pattern
- **Derive macro**: Migration structs use `#[derive(DeriveMigrationName)]` to auto-generate the migration name from the module path
- **Trait implementation**: All migrations implement `MigrationTrait` with `up()` and `down()` methods
- **Async trait**: The impl block uses the `#[async_trait::async_trait]` attribute
- **Return type**: Both `up` and `down` return `Result<(), DbErr>`
- **Schema operations**: Use SeaORM's builder pattern via `SchemaManager` (e.g., `Table::alter()`, `Table::create()`)
- **Iden enums**: Local `#[derive(Iden)]` enums define table and column identifiers scoped to each migration module

### Framework Conventions (from repo-level analysis)
- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)

### Test Conventions (from `tests/api/advisory.rs` sibling analysis)
- **Assertion style**: Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Database tests**: Integration tests hit a real PostgreSQL test database
- **Error cases**: Tests include status code assertions for error scenarios (e.g., `StatusCode::NOT_FOUND`)

## CONVENTIONS.md Findings

The repository root contains a `CONVENTIONS.md` file. Key items that would be extracted:
- CI check commands (for Step 9 verification): expected to include `cargo build`, `cargo clippy`, `cargo fmt --check`, and `cargo test`
- Any migration-specific naming or structure rules
- Code generation commands (if any)

## Convention Conflicts

No convention conflicts detected between the task description/Implementation Notes and the discovered conventions. The task explicitly instructs following the `m0001_initial` pattern, which aligns with all discovered conventions.
