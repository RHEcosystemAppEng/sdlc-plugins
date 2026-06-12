# Discovered Conventions

## Step 0 -- Validate Project Configuration

Project Configuration validated in `claude-md-mock.md`:
- Repository Registry: present with `trustify-backend` entry (Serena instance: `serena_backend`, Path: `./`)
- Jira Configuration: present with Project key `TC`, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: present with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance

All required sections are present. Proceeding.

## Step 1.5 -- Verify Description Integrity

No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

(In a real run, this step would call `jira.get_issue_comments(TC-9201)` to look for a comment starting with `[sdlc-workflow] Description digest:`. Since we are not calling external tools, we note the warning and proceed.)

## CONVENTIONS.md Lookup

The repository root at `./` contains a `CONVENTIONS.md` file (listed in the repo structure). In a real run, this file would be read via Serena or Read tool. No verification commands were extracted since the file content is not available in the eval fixture.

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

Based on analysis of the `modules/fundamental/src/` directory structure and sibling modules (`sbom/`, `advisory/`, `package/`):

- **Module structure:** Every domain module follows `model/ + service/ + endpoints/` sub-directory layout. Each sub-directory has a `mod.rs` that re-exports public types.
- **Model pattern:** Each model sub-directory has a `mod.rs` registering sub-modules, with individual files per struct (e.g., `summary.rs` for `SbomSummary`, `details.rs` for `SbomDetails`). New model files must be registered as `pub mod <name>;` in the parent `mod.rs`.
- **Service pattern:** Service structs (e.g., `SbomService`, `AdvisoryService`) define methods like `fetch`, `list`, `search`. Methods accept `&self`, an entity ID or filter params, and a `tx: &Transactional<'_>` parameter for transaction propagation.
- **Endpoint pattern:** Each endpoint is a separate file (e.g., `list.rs`, `get.rs`). Handlers extract path params via `Path<Id>`, call the corresponding service method, and return JSON. Route registration is centralized in each module's `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.
- **Error handling:** All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`. Errors are wrapped using `.context()` for descriptive messages.
- **Response types:** Single-entity endpoints return the struct directly (Axum `Json` handles serialization). List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Naming conventions:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`). Endpoint handler functions are named after the action (e.g., `get`, `list`).
- **Import organization:** Local crate imports grouped separately from external dependencies.
- **Framework:** Axum for HTTP routing, SeaORM for database access.
- **Entity layer:** Database entities are defined in `entity/src/` using SeaORM. Join tables (e.g., `sbom_advisory.rs`, `sbom_package.rs`) model many-to-many relationships.

### Test Conventions

Based on analysis of sibling test files in `tests/api/` (`sbom.rs`, `advisory.rs`, `search.rs`):

- **Location:** Integration tests live in `tests/api/` with one file per domain (e.g., `sbom.rs`, `advisory.rs`).
- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization and field assertions.
- **Error cases:** All endpoint test files include a 404 test verifying `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent resource IDs.
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
- **Test infrastructure:** Tests hit a real PostgreSQL test database (integration-level, not mocked).
- **Documentation:** Every test function should have a `///` doc comment explaining what it verifies (per skill Step 7 requirements).
- **Test body structure:** Non-trivial tests should use `// Given`, `// When`, `// Then` section comments.

### Cross-Section Reference Consistency

Verified file path references across task description sections:

- Entity `AdvisoryService` -- Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs` -- **consistent**
- Entity `SeveritySummary` model -- Files to Create: `modules/fundamental/src/advisory/model/severity_summary.rs`, Implementation Notes references `modules/fundamental/src/advisory/model/summary.rs` for existing `AdvisorySummary` struct with `severity` field -- **consistent** (different files, different entities)
- Entity endpoint registration -- Files to Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`, Implementation Notes: `modules/fundamental/src/advisory/endpoints/mod.rs` -- **consistent**
- Entity endpoint handler -- Files to Create: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, Implementation Notes references `modules/fundamental/src/advisory/endpoints/get.rs` for pattern reference -- **consistent** (different files, pattern reference vs. new file)
- Entity model registration -- Files to Modify: `modules/fundamental/src/advisory/model/mod.rs` -- **no conflicting references**

No cross-section reference inconsistencies detected.
