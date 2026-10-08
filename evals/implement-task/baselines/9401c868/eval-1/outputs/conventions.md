# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present, contains Project key `TC`, Cloud ID, Feature issue type ID `10142`
3. **Code Intelligence** -- present, tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` with `rust-analyzer`

All checks pass. Proceeding.

## Step 1 -- Parsed Task Fields

- **Key**: TC-9201
- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none
- **GitHub Issue custom field**: `customfield_10747` (configured but would need to read field value from API response)
- **Git Pull Request custom field**: `customfield_10875`
- **webUrl**: `https://redhat.atlassian.net/browse/TC-9201`

## Step 1.5 -- Description Digest Check

Would fetch issue comments via `jira.get_issue_comments(TC-9201)` and search for
comments starting with `[sdlc-workflow] Description digest:`. If found, would extract
the tagged digest, compute the current description digest using
`python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags and hex
values. On match, proceed silently. On mismatch, prompt the user to proceed or stop.
If no digest comment found, log warning and proceed (backward compatibility).

## Step 4 -- Convention Conformance Analysis

### Source: Sibling endpoint files

Analyzed: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`, and `modules/fundamental/src/sbom/endpoints/get.rs`

### Naming Conventions

- **Files**: lowercase snake_case (`get.rs`, `list.rs`, `summary.rs`, `details.rs`)
- **Structs**: PascalCase (`AdvisorySummary`, `SbomDetails`, `PaginatedResults`)
- **Functions/methods**: snake_case, verb_noun pattern (`fetch`, `list`, `search`, `severity_summary`)
- **Endpoint handlers**: named after their action (e.g., `get`, `list`), receiving path params via Axum `Path<Id>` extractor
- **Route paths**: RESTful, kebab-case for multi-word segments (`/api/v2/sbom/{id}/advisory-summary`)
- **Test functions**: `test_` prefix, descriptive snake_case (`test_empty_sbom_risk_score`)

### Error Handling

- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` pattern (anyhow-style)
- 404 errors returned when entity not found, consistent with existing SBOM/advisory endpoints

### Module Structure

- Each domain follows `model/ + service/ + endpoints/` structure
- `model/mod.rs` re-exports sub-modules (`pub mod summary;`, `pub mod details;`)
- `endpoints/mod.rs` registers routes via `Router::new().route("/path", get(handler))`
- `service/mod.rs` or named service file contains the service struct with methods

### Import Organization

- Framework imports first (axum, serde, sea-orm)
- Internal crate imports next (common, entity)
- Local module imports last

### Response Patterns

- Single-entity endpoints return the struct directly (Axum `Json<T>` handles serialization)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Serde `Serialize`/`Deserialize` derives on all response types

### Test Conventions

- Integration tests in `tests/api/` directory, one file per domain
- Tests hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status checks
- Response body parsed and compared with `assert_eq!` on specific field values

### CONVENTIONS.md

Would check for `./CONVENTIONS.md` in the trustify-backend repository root. The repo structure lists a `CONVENTIONS.md` file. Would read it for CI check commands, code generation commands, and additional conventions. Would extract verification commands for use in Step 9.

### Documentation Files Identified

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/api.md` -- REST API reference (would need updating with new endpoint)
- `docs/architecture.md` -- system architecture overview

### Rust-Specific Conventions

- **Framework**: Axum for HTTP routing and handlers
- **ORM**: SeaORM for database queries
- **Serialization**: serde with `Serialize`/`Deserialize` derives
- **Transactional pattern**: methods accept `tx: &Transactional<'_>` for database operations
- **ID type**: `Id` type used for entity identifiers, extracted via `Path<Id>`
- **Caching**: tower-http caching middleware configured in route builders

### Crate Name Resolution

Would run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve crate names for modified files rather than deriving from the nearest `Cargo.toml`. Files under `modules/fundamental/src/` belong to whatever crate name is declared in `modules/fundamental/Cargo.toml`. The test file under `tests/` belongs to the crate in `tests/Cargo.toml`.
