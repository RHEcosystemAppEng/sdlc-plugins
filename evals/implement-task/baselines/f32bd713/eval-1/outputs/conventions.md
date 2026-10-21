# Convention Conformance Analysis

Conventions discovered from sibling analysis in the trustify-backend repository.
Siblings examined: `sbom/` module (model, service, endpoints), `advisory/` existing
files, `package/` module, and `tests/api/` test files.

## Naming Conventions

- **Files**: lowercase snake_case (`summary.rs`, `details.rs`, `sbom.rs`)
- **Structs/Types**: PascalCase (`SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- **Functions/Methods**: snake_case verb_noun pattern (`fetch`, `list`, `search`, `ingest`)
- **Service structs**: `<Domain>Service` (e.g., `SbomService`, `AdvisoryService`, `PackageService`)
- **Test files**: match the domain name (`sbom.rs`, `advisory.rs`, `search.rs`)
- **Model modules**: each domain has `model/mod.rs` re-exporting submodules (`summary.rs`, `details.rs`)

## Module Structure

- Each domain module follows the `model/ + service/ + endpoints/` tripartite structure
- `model/mod.rs` registers submodules with `pub mod <name>;`
- `service/mod.rs` or `service/<domain>.rs` contains the service implementation
- `endpoints/mod.rs` registers routes; individual handler files per operation (`list.rs`, `get.rs`)

## Error Handling

- All handlers return `Result<T, AppError>`
- Errors wrapped with `.context()` for descriptive messages
- `AppError` enum defined in `common/src/error.rs`, implements `IntoResponse`

## Endpoint Patterns

- Route registration in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`
- Path parameters extracted via `Path<Id>`
- Handlers call service methods, return JSON via Axum's `Json` extractor
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

## Service Method Patterns

- Service methods take `&self`, domain-specific ID parameters, and `tx: &Transactional<'_>`
- Methods like `fetch` and `list` are the standard operations
- Services interact with SeaORM entities for database access

## Response Types

- Single-item endpoints return the struct directly (Axum `Json` handles serialization)
- List endpoints return `PaginatedResults<T>`
- 404 errors returned via `AppError` when entity not found

## Import Organization

- Standard library imports first
- External crate imports second
- Internal crate imports third (from `common`, `entity`, etc.)

## Test Conventions

- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`
- One test file per domain area
- No parameterized test usage observed in siblings -- will not introduce parameterized tests

## Documentation

- Structs documented with `///` doc comments (Rust convention)
- Per SKILL.md guidance: every new struct, type, and public function must have a `///` doc comment
- Per SKILL.md guidance: every test function must have a `///` doc comment (overrides sibling patterns)
- Per SKILL.md guidance: non-trivial tests use `// Given`, `// When`, `// Then` section comments

## CONVENTIONS.md

- A `CONVENTIONS.md` file exists at the repository root per the repo structure
- Would be read for CI check commands and verification commands
- Would be read for code generation commands

## Skill Guidance Overrides

- SKILL.md requires value-based assertions (not just `.any()` or length checks) -- this overrides any sibling patterns using length-only checks
- SKILL.md requires `///` doc comments on all test functions -- this is a new standard regardless of sibling practice
- SKILL.md requires given-when-then section comments for non-trivial tests
