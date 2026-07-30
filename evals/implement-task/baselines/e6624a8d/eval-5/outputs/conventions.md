# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Migration pattern (from `migration/src/m0001_initial/mod.rs`)
- **Structure:** Each migration lives in its own subdirectory under `migration/src/` named `m<NNNN>_<description>/mod.rs`
- **Trait implementation:** Every migration module implements `MigrationTrait` with two required methods: `up` (apply) and `down` (rollback)
- **Naming:** Migration directories follow the pattern `m<zero-padded-number>_<snake_case_description>` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Registration:** Migrations are registered in `migration/src/lib.rs` by adding `Box::new(m<NNNN>_<description>::Migration)` to the `vec![]` returned by the `migrations()` function
- **Module declaration:** Each new migration directory must be declared as `mod m<NNNN>_<description>;` in `migration/src/lib.rs`

### Database framework
- **ORM:** SeaORM is used for all database operations
- **Schema changes:** Use `TableAlterStatement` via `manager.alter_table(...)` for column-level DDL operations
- **Column definitions:** Use `ColumnDef::new(Entity::Column)` to define column types for `down` (rollback) methods
- **Entity references:** Column and table identifiers come from entity enums (e.g., `Advisory::Table`, `Advisory::Status`)

### Error handling
- **Result types:** All handlers use `Result<T, AppError>` with `.context()` for wrapping (from `common/src/error.rs`)
- **Error enum:** `AppError` implements `IntoResponse` for Axum integration

### Naming conventions
- **Service methods:** Follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_packages`)
- **Module structure:** Domain modules follow `model/ + service/ + endpoints/` structure

### Framework conventions
- **HTTP:** Axum for HTTP routing and request handling
- **Responses:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers:** Shared filtering, pagination, and sorting via `common/src/db/query.rs`

## Test Conventions

### Integration tests (from `tests/api/`)
- **Location:** Integration tests reside in `tests/api/` with one file per domain (e.g., `advisory.rs`, `sbom.rs`, `search.rs`)
- **Database:** Tests hit a real PostgreSQL test database
- **Assertion style:** Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code checks
- **Caching:** `tower-http` caching middleware is used; cache configuration in endpoint route builders

## CONVENTIONS.md
- A `CONVENTIONS.md` file exists at the repository root; its contents would be read and followed during implementation. Verification commands from its CI checks section would be extracted and run before committing.
