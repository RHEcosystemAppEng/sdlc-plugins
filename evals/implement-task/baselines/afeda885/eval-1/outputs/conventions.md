# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

Project Configuration validated from CLAUDE.md:
- Repository Registry: present (trustify-backend, Serena instance: serena_backend, path: ./)
- Jira Configuration: present (Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID: 10142)
- Code Intelligence: present (serena_backend instance, rust-analyzer)

All required sections found. Proceeding.

## Step 1.5 -- Description Digest Verification

> No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

No digest comment was located on the issue. Proceeding with implementation.

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

- **Framework**: Axum for HTTP routing, SeaORM for database access (PostgreSQL)
- **Module structure**: Each domain module follows a consistent `model/ + service/ + endpoints/` three-layer pattern (observed in `sbom/`, `advisory/`, `package/`)
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping for descriptive error chains; `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`
- **Naming -- service methods**: Follow `verb_noun` pattern (e.g., `fetch`, `list`, `search` on `AdvisoryService`; `fetch`, `list`, `ingest` on `SbomService`)
- **Naming -- endpoint files**: Named by HTTP action (`get.rs`, `list.rs`) corresponding to the endpoint's purpose
- **Naming -- model files**: Named by type role (`summary.rs`, `details.rs`) -- the new file `severity_summary.rs` follows this pattern
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern; `server/main.rs` mounts all modules
- **Response types**: Single-entity endpoints return the struct directly via Axum's `Json` extractor; list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Service method signatures**: Methods take `&self`, domain-specific ID parameters, and `tx: &Transactional<'_>` for transaction propagation
- **Path parameters**: Extracted via Axum's `Path<Id>` extractor pattern (observed in `get.rs` endpoints)
- **Module registration**: New model sub-modules registered via `pub mod <name>;` in the parent `mod.rs`
- **Import organization**: External crate imports first, then internal crate imports, then local module imports (inferred from Rust convention and project structure)
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Caching**: Uses `tower-http` caching middleware in route builders

### Test Conventions

- **Test location**: Integration tests live in `tests/api/` directory, one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- **Test style**: Integration tests hit a real PostgreSQL test database (not mocks)
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks followed by body deserialization
- **Error case coverage**: Include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent resource IDs
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Response validation**: Validate specific field values (critical, high, medium, low, total) not just counts
- **New file naming**: New test file `advisory_summary.rs` follows the pattern of sibling files (`sbom.rs`, `advisory.rs`, `search.rs`)

### CONVENTIONS.md

A `CONVENTIONS.md` file exists at the repository root. It should be read for:
- CI check commands (formatting, linting, compilation)
- Code generation commands
- Any additional project-specific conventions

Since we cannot read the actual file in this eval, we note its presence and would consult it during real implementation.

### Documentation Files Identified

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (directly impacted by the new endpoint)

### Cross-Section Reference Consistency

- Entity `AdvisoryService` -- Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`; Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- Entity `SeveritySummary` (model) -- Files to Create: `modules/fundamental/src/advisory/model/severity_summary.rs`; Implementation Notes: references `AdvisorySummary` in `model/summary.rs` as source of severity field -- CONSISTENT (different entities, no conflict)
- Entity `endpoints/mod.rs` -- Files to Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`; Implementation Notes: `modules/fundamental/src/advisory/endpoints/mod.rs` -- CONSISTENT
- All file path references are consistent across Description, Files to Modify, Files to Create, and Implementation Notes sections.
