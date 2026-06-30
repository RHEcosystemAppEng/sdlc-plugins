# Conventions Discovered from Sibling Analysis

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

1. **Module structure**: Each migration lives in its own directory under `migration/src/` named with a sequential prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`).
2. **Entry point**: Each migration module has a `mod.rs` file that implements the `MigrationTrait` trait from SeaORM.
3. **Required methods**: Every migration must implement both `up` (apply) and `down` (rollback) methods.
4. **Registration**: Migrations are registered in `migration/src/lib.rs` by adding them to the `vec![]` returned by the `migrations()` function.
5. **Table operations**: Uses SeaORM's `TableAlterStatement` API for schema changes (e.g., `Table::alter().table(...).drop_column(...)`).
6. **Column references**: Column and table identifiers reference the entity enums (e.g., `Advisory::Table`, `Advisory::Status`).

## Project-Wide Conventions (from repository structure)

1. **Framework**: Axum for HTTP, SeaORM for database ORM.
2. **Module pattern**: Each domain module follows a `model/ + service/ + endpoints/` structure.
3. **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping.
4. **Entity organization**: SeaORM entities live in `entity/src/` with one file per table.
5. **Testing**: Integration tests reside in `tests/api/` and run against a real PostgreSQL test database.
6. **Code intelligence**: rust-analyzer is configured via Serena for code inspection.

## Workflow Conventions (from sdlc-workflow)

1. **Branch naming**: Task branches are named after the Jira task issue ID (e.g., `TC-9205`).
2. **Feature branch targeting**: When a task has a Target Branch that is not `main`, the task branch is created from that feature branch and the PR targets it with `--base`.
3. **Commit format**: Conventional Commits with Jira ID footer and `Assisted-by: Claude Code` trailer.
4. **PR description**: Must include `## Summary` with bullet points and `## Jira` section with link.
5. **Code inspection before modification**: All files must be inspected via Serena or Read/Grep/Glob before being modified (constraint 5.2).
6. **Scope containment**: Changes must be scoped to files listed in Files to Modify and Files to Create (constraint 5.1).
