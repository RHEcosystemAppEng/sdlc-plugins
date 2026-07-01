## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and a service method on `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` table for severity data, deduplicates by advisory ID, and aggregates counts by severity level (Critical, High, Medium, Low). This provides the data layer for the new advisory summary endpoint (TC-9001).

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `AdvisorySeveritySummary` struct
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method that performs the aggregation query

## Implementation Notes
- The `AdvisorySeveritySummary` struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone` consistent with existing model structs like `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`.
- The aggregation query must join `sbom_advisory` (from `entity/src/sbom_advisory.rs`) with `advisory` (from `entity/src/advisory.rs`) to access the severity field.
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT advisory_id` or equivalent SeaORM approach to ensure each advisory is counted only once per severity level.
- The service method should return `AppError` with `.context()` wrapping, following the error handling pattern in `common/src/error.rs`. See the existing `SbomService` methods in `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern (fetch, list, ingest methods).
- The severity field on `AdvisorySummary` (in `modules/fundamental/src/advisory/model/summary.rs`) shows how severity is represented in the existing codebase — use the same severity type/enum for consistent classification.
- Use shared query builder helpers from `common/src/db/query.rs` if applicable for filtering.
- Per CONVENTIONS.md: follow the `model/ + service/ + endpoints/` module pattern — this task covers the model and service layers only.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md: all handlers/service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; reuse the same severity type/enum for classification
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend with the new aggregation method; follow its established patterns for database queries and error handling
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for the aggregation join query
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] `SbomService::advisory_severity_summary(sbom_id)` returns correct severity counts for a given SBOM
- [ ] Advisory deduplication by advisory ID is applied (same advisory linked multiple times is counted once)
- [ ] Method returns `AppError` when the SBOM ID does not exist

## Test Requirements
- [ ] Unit test: verify `AdvisorySeveritySummary` serialization produces expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Service test: verify aggregation correctly counts advisories by severity level
- [ ] Service test: verify deduplication — duplicate advisory links produce correct counts
- [ ] Service test: verify error returned for non-existent SBOM ID

## Dependencies
- None

---

> [sdlc-workflow] Description digest: (simulated) The digest would be posted as a Jira comment after task creation per the description-digest-protocol. Format: `[sdlc-workflow] Description digest: sha256-md:<64-hex-chars>`
