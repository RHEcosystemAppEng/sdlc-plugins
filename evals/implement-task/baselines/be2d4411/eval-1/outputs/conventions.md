# Discovered Conventions (from Sibling Analysis)

## Step 4 -- Convention Conformance Analysis

### Production Code Conventions

#### Module Structure
- Each domain module follows a strict `model/ + service/ + endpoints/` structure under `modules/fundamental/src/<domain>/`.
- The `model/` directory contains a `mod.rs` that re-exports sub-modules (e.g., `summary.rs`, `details.rs`).
- The `service/` directory contains a `mod.rs` and a domain-named file (e.g., `sbom.rs`, `advisory.rs`) with the service implementation.
- The `endpoints/` directory contains a `mod.rs` for route registration, plus individual handler files (e.g., `list.rs`, `get.rs`).

#### Naming Conventions
- Service methods follow the `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`).
- Model structs use PascalCase domain names (e.g., `SbomSummary`, `AdvisorySummary`, `AdvisoryDetails`, `SeveritySummary`).
- Endpoint handler files are named after the HTTP operation or resource they handle (e.g., `get.rs`, `list.rs`, `severity_summary.rs`).
- Test files mirror the endpoint/feature name with underscores (e.g., `advisory_summary.rs`).

#### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.
- Errors are wrapped with `.context()` for descriptive error messages.
- `AppError` implements `IntoResponse` for Axum integration.

#### Endpoint Patterns (from sibling analysis of `endpoints/get.rs`, `endpoints/list.rs`)
- Path parameters extracted via Axum's `Path<Id>` extractor.
- Service called with extracted parameters and a transactional context (`tx: &Transactional<'_>`).
- Response returned directly as the struct (Axum's `Json` extractor handles serialization via Serde).
- Routes registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.

#### Response Types
- Single-entity endpoints return the domain struct directly (e.g., `AdvisoryDetails`, `SeveritySummary`).
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

#### Import Organization
- External crate imports first, then internal module imports.
- Axum extractors (`Path`, `Json`, `State`) imported from `axum::extract`.
- SeaORM types imported from `sea_orm`.

#### Database Patterns
- SeaORM entities defined in `entity/src/` (e.g., `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`).
- Join tables follow the `<entity1>_<entity2>.rs` naming pattern (e.g., `sbom_advisory.rs`).
- Queries use SeaORM's query builder with `.find()`, `.filter()`, `.join()` patterns.

### Test Conventions (from sibling test analysis of `tests/api/sbom.rs`, `tests/api/advisory.rs`)

#### Assertion Style
- All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for success cases.
- Response body deserialized after status check for field-level validation.
- Value-based assertions preferred over length-only checks.

#### Response Validation
- Tests validate specific field values, not just counts.
- JSON responses deserialized into the expected struct type for type-safe assertions.

#### Error Cases
- All endpoint test files include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Non-existent resource IDs tested to verify proper error handling.

#### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`, `test_get_sbom_not_found`).

#### Test Setup
- Integration tests hit a real PostgreSQL test database.
- Test fixtures created programmatically (database seeding) before assertions.
- Tests are independent -- each test sets up its own data.

#### Test Organization
- One test file per feature area in `tests/api/`.
- Tests grouped by success/failure scenarios within each file.

#### Parameterized Tests
- No evidence of `#[rstest]` or parameterized test usage in sibling test files -- individual test functions are the convention.

### CONVENTIONS.md
- A `CONVENTIONS.md` file exists at the repository root per the repo structure.
- It would be read during implementation for explicit project-level conventions and CI check commands.
- No CI verification commands were extracted since this is a simulated run (file contents not available).

### Documentation Files Identified
- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (may need updating for new endpoint)
