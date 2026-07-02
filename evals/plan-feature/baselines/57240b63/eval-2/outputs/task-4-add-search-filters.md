## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint (GET /api/v2/search) so users can
narrow results by entity type, date range, and severity. The feature description
requests "some kind of filtering capability" but provides no specification of which
filters to support (see Ambiguity 3 in the impact map). This task implements a set
of filters based on the existing entity data model.

**Assumption (pending clarification):** The following filters are implemented based
on fields available in the existing entity model. The product owner should confirm:
1. Which filters are required (entity type, date range, severity, or others?)
2. How filters compose (AND logic assumed — all filters must match)
3. Whether additional entity-specific filters are needed (e.g., license type for packages)

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters to GET /api/v2/search: `entity_type` (enum: sbom, advisory, package), `date_from` and `date_to` (ISO 8601), `severity` (string matching advisory severity)
- `modules/search/src/service/mod.rs` — Accept filter parameters in the search method and apply them as WHERE clause predicates in the database query

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type`, `date_from`, `date_to`, `severity`. All parameters are optional and additive (AND composition). When no filters are provided, behavior is unchanged (backward compatible).

## Implementation Notes
- Use the shared query builder helpers in `common/src/db/query.rs` for filtering and
  pagination. Inspect the existing helpers to understand how filter predicates are
  constructed — the module already provides shared filtering, pagination, and sorting
  utilities.
- Define filter parameter types using Axum's `Query` extractor with `serde::Deserialize`.
  Follow the pattern used in existing list endpoints:
  - `modules/fundamental/src/sbom/endpoints/list.rs` — GET /api/v2/sbom list endpoint
  - `modules/fundamental/src/advisory/endpoints/list.rs` — GET /api/v2/advisory list endpoint
- Entity type filter: use an enum (`SearchEntityType`) with variants for sbom, advisory,
  package. When applied, restrict the search to the specified entity table only.
- Date range filter: apply to the entity's created/updated timestamp column. Use
  `chrono::NaiveDateTime` or `chrono::DateTime<Utc>` for date parameter parsing.
- Severity filter: apply only when searching advisories (see `AdvisorySummary` severity
  field in `modules/fundamental/src/advisory/model/summary.rs`). When entity_type is
  not "advisory", the severity filter is silently ignored.
- All filter parameters must be optional — omitting a filter returns unfiltered results
  for that dimension, preserving backward compatibility.
- Error handling: return `AppError` with descriptive context for invalid filter values
  (e.g., malformed dates, unknown entity types). See `common/src/error.rs` for the
  AppError enum.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing code before
  modifying; changes scoped to listed files only.

**Conventions (from Key Conventions):**

Per Key Conventions §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per Key Conventions §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust source file scope.

Per Key Conventions §Endpoint registration: each module's `endpoints/mod.rs` registers routes.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers; use existing filter predicate construction instead of writing custom WHERE clause logic
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of list endpoint with query parameter extraction pattern to follow
- `modules/fundamental/src/advisory/endpoints/list.rs` — Example of list endpoint with similar query parameter handling
- `common/src/error.rs` — AppError enum for consistent error responses on invalid filter values

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type`, `date_from`, `date_to`, and `severity` query parameters
- [ ] Entity type filter restricts results to the specified entity type (sbom, advisory, or package)
- [ ] Date range filter restricts results to entities within the specified date range
- [ ] Severity filter restricts advisory results by severity level
- [ ] Filters compose with AND logic (all active filters must match)
- [ ] Omitting all filters returns the same results as the current unfiltered search (backward compatible)
- [ ] Invalid filter values return appropriate error responses

## Test Requirements
- [ ] Integration test: search with entity_type=sbom returns only SBOM results
- [ ] Integration test: search with entity_type=advisory returns only advisory results
- [ ] Integration test: search with date_from and date_to returns only results within the date range
- [ ] Integration test: search with severity filter returns only matching advisories
- [ ] Integration test: search with multiple filters applies AND composition
- [ ] Integration test: search with no filters returns all results (backward compatibility)
- [ ] Integration test: search with invalid filter value returns an error response

## Verification Commands
- `cargo test --test search` — All search integration tests pass

## Dependencies
- None (can be developed independently; benefits from Task 1 indexes and Task 2 query optimizations)

## additional_fields
- priority: Normal
- fixVersions: ["RHTPA 1.6.0"]
- labels: ["ai-generated-jira"]
---

[sdlc-workflow] Description digest: sha256-md:c4d80c1a22385843495fcc57e75430d48cab61bad7aebf8249726d68d1ba5c14
