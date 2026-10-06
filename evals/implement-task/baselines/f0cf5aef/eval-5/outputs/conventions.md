# Conventions Discovered from Sibling Analysis

## Source of Analysis

Primary sibling: `migration/src/m0001_initial/mod.rs` (the only existing migration, serving as the pattern for all new migrations)

Secondary context: repository-level conventions from `repo-backend.md` Key Conventions section, and the project's `CONVENTIONS.md` (if present at repository root).

## Discovered Conventions

### Migration Module Structure

- Each migration lives in its own directory under `migration/src/` named `m<NNNN>_<descriptive_name>/`
- Each migration directory contains a single `mod.rs` file
- Numbering is sequential and zero-padded to 4 digits (m0001, m0002, ...)
- Naming uses snake_case with a descriptive suffix (e.g., `m0001_initial`, `m0002_drop_advisory_status`)

### Migration Implementation Pattern

- Use `#[derive(DeriveMigrationName)]` on the Migration struct for automatic name derivation
- Implement `MigrationTrait` from `sea_orm_migration::prelude::*`
- Use `#[async_trait::async_trait]` attribute for the async trait implementation
- Both `up` and `down` methods are required -- `up` applies the migration, `down` reverses it
- Methods return `Result<(), DbErr>`
- Migrations define their own local `#[derive(Iden)]` enums for table/column identifiers rather than importing from the entity crate (keeps migrations self-contained and immune to future entity changes)

### Migration Registration

- Module declared with `mod m<NNNN>_<name>;` in `migration/src/lib.rs`
- Migration added to the `vec![]` in the `migrations()` function as `Box::new(m<NNNN>_<name>::Migration)`
- Order in the vec determines execution order -- append new migrations at the end

### Framework Conventions (Repository-Wide)

- **Framework**: Axum for HTTP, SeaORM for database ORM and migrations
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Module pattern**: `model/ + service/ + endpoints/` structure for domain modules
- **Testing**: Integration tests in `tests/api/` using real PostgreSQL; assertion pattern `assert_eq!(resp.status(), StatusCode::OK)`

### Naming Conventions

- Functions: `snake_case` (Rust standard)
- Types/Structs: `PascalCase` (Rust standard)
- Files: `snake_case` with `.rs` extension
- Modules: `snake_case` directory names

### Error Handling (Migrations)

- Migration methods return `Result<(), DbErr>` directly
- Use `?` operator for error propagation (standard Rust)
- No explicit `.context()` wrapping in migrations (that pattern applies to service/handler code)

### Documentation

- Document migration structs with `///` doc comments explaining what the migration does and why
- Document `up` and `down` methods with `///` doc comments

### Import Organization

- Use glob import `use sea_orm_migration::prelude::*;` for migration prelude
- Use `use async_trait::async_trait;` or attribute-based `#[async_trait::async_trait]`

## Convention Conflicts

None detected. The task description's Implementation Notes align with the patterns observed in the sibling migration.

## Skill Guidance Overrides

- **Test documentation**: The skill requires `///` doc comments on every test function, even if sibling tests lack them. This will be applied to any tests written for this migration.
- **Value-based assertions**: The skill prefers asserting on actual values over length-only checks. Migration tests should verify column presence/absence, not just migration success status.
