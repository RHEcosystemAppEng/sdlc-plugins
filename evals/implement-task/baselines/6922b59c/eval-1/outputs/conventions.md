# Convention Conformance Analysis for TC-9201

Conventions discovered from sibling analysis of the trustify-backend repository.
These serve as binding reference during implementation (Step 6) and test writing (Step 7).

## Source Files Analyzed

### Endpoint siblings (modules/fundamental/src/advisory/endpoints/)
- `get.rs` -- GET /api/v2/advisory/{id} handler
- `list.rs` -- GET /api/v2/advisory list handler
- `mod.rs` -- route registration

### Model siblings (modules/fundamental/src/advisory/model/)
- `summary.rs` -- AdvisorySummary struct (includes severity field)
- `details.rs` -- AdvisoryDetails struct

### Service siblings (modules/fundamental/src/advisory/service/)
- `advisory.rs` -- AdvisoryService with fetch, list, search methods

### Cross-module siblings (modules/fundamental/src/sbom/)
- `endpoints/get.rs` -- GET /api/v2/sbom/{id} handler (same path-param pattern)
- `endpoints/list.rs` -- GET /api/v2/sbom list handler
- `service/sbom.rs` -- SbomService with fetch, list, ingest methods

### Test siblings (tests/api/)
- `advisory.rs` -- advisory endpoint integration tests
- `sbom.rs` -- SBOM endpoint integration tests

---

## Discovered Conventions

### Naming Conventions
- **Functions:** `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- **Handler functions:** Named after the action, e.g., `get`, `list`; for new sub-resources, use descriptive names like `severity_summary`
- **Structs:** PascalCase with domain prefix (e.g., `AdvisorySummary`, `SbomDetails`, `SeveritySummary`)
- **Files:** snake_case matching the primary struct or function (e.g., `severity_summary.rs`)
- **Test functions:** `test_<description>` pattern (e.g., `test_valid_sbom_severity_counts`)
- **Modules:** Registered in parent `mod.rs` with `pub mod <name>;`

### Error Handling
- All handlers return `Result<T, AppError>`
- Errors wrapped with `.context("descriptive message")` using anyhow-style context
- `AppError` enum defined in `common/src/error.rs`, implements `IntoResponse`
- Not-found cases return appropriate HTTP 404 via AppError variant
- Pattern: `service.method(id, &tx).await.context("failed to ...")?`

### Service Method Signatures
- Instance methods on service struct: `&self`
- ID parameter: typed as `Id`
- Transaction parameter: `tx: &Transactional<'_>`
- Return type: `Result<T, anyhow::Error>` or `Result<T, AppError>`
- Pattern: `pub async fn method_name(&self, param: Id, tx: &Transactional<'_>) -> Result<T, Error>`

### Endpoint Handler Signatures
- Path parameters extracted via `Path<Id>` (Axum extractor)
- Service obtained from state/extension
- Returns `Result<Json<T>, AppError>`
- Pattern: `pub async fn handler(Path(id): Path<Id>, service: ...) -> Result<Json<T>, AppError>`

### Route Registration
- In `endpoints/mod.rs`: `Router::new().route("/path", get(handler))`
- Sub-resource routes use nested paths
- Routes auto-mount via module registration in `server/src/main.rs`

### Response Types
- Single-entity responses: return struct directly via `Json<T>`
- List responses: return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- All response structs derive `Serialize` (and typically `Deserialize`)

### Import Organization
- Standard library imports first
- External crate imports second (axum, serde, sea_orm, anyhow)
- Internal module imports last (crate::, super::)
- Grouped by blank lines between sections

### Model Struct Patterns
- Derive `Serialize, Deserialize, Clone, Debug`
- Use `#[serde(rename_all = "camelCase")]` for JSON field naming (or snake_case if consistent with siblings)
- Documentation comment on every public struct
- Fields are public

### Database Query Patterns
- SeaORM for database access
- Join table queries use entity relationships
- Entity definitions in `entity/src/` (e.g., `sbom_advisory.rs`)
- Queries use `.find_related()` or manual joins via `JoinType`

### Test Conventions
- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`
- Error case coverage: test both success and 404/error paths
- Setup: create test fixtures before assertions
- No parameterized test framework observed in siblings -- use individual test functions

### Documentation
- Doc comments (`///`) on all public structs, methods, and functions
- One-line description of purpose is sufficient
- For test functions: doc comment explaining what the test verifies (skill guidance -- applies even if siblings lack this)

---

## Skill Guidance Overrides

The following skill-mandated conventions override sibling patterns where they conflict:

1. **Test documentation:** Every test function gets a `///` doc comment, regardless of whether sibling tests have them. This is explicitly required by Step 7 of the skill.

2. **Value-based assertions:** Prefer asserting on specific values (e.g., `assert_eq!(body.critical, 3)`) over length-only checks (e.g., `assert!(body.total > 0)`). This is skill guidance that takes precedence over any sibling pattern using `.any()` or length checks.

3. **Given-When-Then comments:** Non-trivial tests include `// Given`, `// When`, `// Then` section comments inside the test body.

---

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` at root. Would read it for:
- CI check commands (e.g., `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`)
- Code generation commands (e.g., OpenAPI spec generation)
- Any additional naming, structural, or testing rules

Verification commands extracted from CONVENTIONS.md would be recorded and executed in Step 9's CI checks sub-step.
