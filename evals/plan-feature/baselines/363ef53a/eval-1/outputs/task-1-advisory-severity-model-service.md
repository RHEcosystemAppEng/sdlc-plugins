## Repository
trustify-backend

## Target Branch
main

## Description
Add an advisory severity summary model and aggregation service method to support the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). This task creates the response struct representing severity counts (critical, high, medium, low, total) and implements the aggregation query in `SbomService` that counts unique advisories per severity level for a given SBOM, using the existing `sbom_advisory` join table.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: critical, high, medium, low, total (all u64); derives Serialize, Deserialize, ToSchema

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries the `sbom_advisory` join table, joins to the `advisory` table for severity, groups by severity, and counts distinct advisory IDs

## Implementation Notes
- The aggregation query should use SeaORM's `select_only()` with `column_as()` and `group_by()` on the advisory severity field from `entity/src/advisory.rs`. Use `entity/src/sbom_advisory.rs` as the join table between SBOMs and advisories.
- Deduplicate by advisory ID as required — use `COUNT(DISTINCT advisory_id)` semantics via SeaORM's `Column::count_distinct()` or equivalent.
- The `AdvisorySeveritySummary` struct should follow the pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct layout and derive macros.
- Return `AppError` with `.context()` wrapping on query failure, consistent with the service layer pattern in `modules/fundamental/src/sbom/service/sbom.rs`.
- Support an optional `threshold` parameter (severity level) to filter counts to only severities at or above the threshold. The service method signature should accept `Option<SeverityThreshold>` and apply a WHERE clause when present.
- Per CONVENTIONS.md §Module pattern: place the model in `model/` and the service method in `service/`, following the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` for any filtering logic. See `modules/fundamental/src/sbom/service/sbom.rs` for established usage patterns. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes a severity field; reference this to understand the severity enum/type used across the codebase
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity definition; the aggregation query joins through this table
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for any filtering logic in the aggregation

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: critical, high, medium, low, total
- [ ] `SbomService::get_advisory_summary` method exists and returns correct severity counts for a given SBOM ID
- [ ] Counts are deduplicated by advisory ID (no double-counting)
- [ ] Method returns `AppError` when the query fails
- [ ] Optional threshold parameter filters severity counts when provided

## Test Requirements
- [ ] Unit test: `get_advisory_summary` returns correct counts for an SBOM with known advisories at each severity level
- [ ] Unit test: `get_advisory_summary` deduplicates advisories linked multiple times
- [ ] Unit test: threshold parameter filters counts correctly (e.g., threshold=high returns only critical and high)

## Dependencies
- None
