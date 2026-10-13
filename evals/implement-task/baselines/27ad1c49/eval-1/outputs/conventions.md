# Conventions Discovered from Sibling Analysis

Conventions discovered during Step 4's convention conformance analysis, organized by
category. These serve as a binding reference during implementation (Step 6) and test
writing (Step 7).

---

## Naming Conventions

- **Files**: lowercase snake_case (e.g., `summary.rs`, `details.rs`, `get.rs`, `list.rs`)
- **Structs/Types**: PascalCase (e.g., `AdvisorySummary`, `SbomDetails`, `PackageSummary`)
- **Functions/Methods**: snake_case verb_noun pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- **Endpoint handlers**: named after the HTTP verb or action (e.g., `get`, `list`) in their own file
- **Module directories**: lowercase singular noun matching the domain entity (e.g., `advisory/`, `sbom/`, `package/`)
- **Test files**: named after the domain entity being tested (e.g., `advisory.rs`, `sbom.rs`, `search.rs`)

## Module Structure

- Each domain module follows the triple-directory pattern: `model/` + `service/` + `endpoints/`
- Each directory has a `mod.rs` that re-exports submodules via `pub mod <name>;` declarations
- Model submodules correspond to response types: `summary.rs`, `details.rs`
- Service submodules contain the primary service struct with its methods
- Endpoint submodules correspond to individual route handlers: `get.rs`, `list.rs`

## Error Handling

- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` (from the `anyhow` or similar error trait)
- `AppError` implements `IntoResponse` for automatic HTTP error responses
- Pattern: `service_call().context("failed to fetch advisory")?`
- Not-found cases return a specific `AppError` variant (likely `AppError::NotFound`) consistent with existing SBOM/advisory endpoints returning 404

## Endpoint Registration

- Routes are registered in each module's `endpoints/mod.rs`
- Pattern: `Router::new().route("/path", get(handler_function))`
- Handlers are imported from sibling files (e.g., `use super::get::get_advisory;`)
- `server/main.rs` mounts all modules -- auto-discovery via module registration means no changes needed there

## Request/Response Patterns

- Path parameters extracted via Axum's `Path<Id>` extractor
- Service methods take `&self`, entity ID, and `tx: &Transactional<'_>` for transaction support
- Single-entity responses return `Json<T>` directly (e.g., `Json<AdvisoryDetails>`)
- List responses return `Json<PaginatedResults<T>>` using `common/src/model/paginated.rs`
- Shared query helpers from `common/src/db/query.rs` provide filtering, pagination, sorting

## Import Organization

- Standard library imports first
- External crate imports second (axum, serde, sea-orm)
- Internal crate imports third (common, entity modules)
- Local module imports last (sibling modules within the same domain)

## Serialization

- Response structs derive `Serialize` (serde) for automatic JSON serialization
- Request structs derive `Deserialize` where applicable
- Commonly also derive `Debug`, `Clone`
- Struct fields use snake_case (serde's default for Rust)

## Database Access

- SeaORM is used for database queries
- Entity definitions in `entity/src/` (e.g., `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`)
- Join tables modeled as separate entities (e.g., `sbom_advisory` for SBOM-Advisory relationships)
- Queries use SeaORM's query builder pattern

## Test Conventions

- Integration tests live in `tests/api/` directory, one file per domain entity
- Tests hit a real PostgreSQL test database (bootstrap provided by test infrastructure)
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status checks
- Response body parsed as the expected struct type for field-level assertions
- Error cases tested: 404 for non-existent IDs, matching existing endpoint patterns
- Test functions are `#[tokio::test]` or `#[test]` depending on async requirements

## Skill Guidance Overrides

The following skill guidance takes precedence over sibling patterns where conflicts exist:

- **Value-based assertions**: Skill requires asserting on specific values, not just collection lengths. If sibling tests use `.len()` or `.any()` checks, prefer explicit value comparisons per skill Step 7 guidance.
- **Test documentation**: Every test function must have a `///` doc comment regardless of whether sibling tests have them (skill Step 7 introduces this as a new standard).
- **Given-When-Then comments**: Non-trivial tests must include `// Given`, `// When`, `// Then` section comments inside the test body.
