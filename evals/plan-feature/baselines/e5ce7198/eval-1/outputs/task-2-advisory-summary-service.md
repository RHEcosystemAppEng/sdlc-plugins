# Task 2: Implement advisory severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add a `get_advisory_summary` method to `SbomService` that queries the database for all advisories linked to a given SBOM, aggregates them by severity level (deduplicating by advisory ID), and returns an `AdvisorySeveritySummary`. This is the core business logic for the advisory summary feature.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_summary` method to `SbomService`

## Implementation Notes
Add the method to the existing `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`. The method should:

1. Accept an SBOM ID parameter and a database connection/transaction
2. Verify the SBOM exists (return 404 error if not found), following the pattern used by existing fetch methods in `SbomService`
3. Query the `sbom_advisory` join table (entity defined in `entity/src/sbom_advisory.rs`) joined with the `advisory` table (`entity/src/advisory.rs`) to get severity values
4. Deduplicate by advisory ID (use `SELECT DISTINCT` or `GROUP BY` on advisory ID)
5. Aggregate counts per severity level (Critical, High, Medium, Low)
6. Return `AdvisorySeveritySummary` with computed counts and total

Use SeaORM query builder patterns from `common/src/db/query.rs` for constructing the query. Use `AppError` from `common/src/error.rs` for error handling with `.context()` wrapping.

Optionally accept a `threshold` parameter (severity level string) to filter counts to only severities at or above the threshold. When threshold is `None`, return all counts.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for all error paths.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Framework: use SeaORM for database queries.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to add the method to; reference existing methods for parameter patterns and error handling
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error type for consistent error handling
- `entity/src/sbom_advisory.rs` — SeaORM entity for the SBOM-Advisory join table
- `entity/src/advisory.rs` — SeaORM entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Advisory counts are deduplicated by advisory ID
- [ ] Counts are correctly aggregated by severity level (critical, high, medium, low)
- [ ] Total field equals sum of all severity counts
- [ ] Optional threshold parameter filters results to only severities at or above the given level

## Test Requirements
- [ ] Unit test with mock data: SBOM with known advisories returns correct severity counts
- [ ] Unit test: duplicate advisory IDs are counted only once
- [ ] Unit test: non-existent SBOM ID returns appropriate error
- [ ] Unit test: threshold parameter filters counts correctly

## Dependencies
- Depends on: Task 1 — Define AdvisorySeveritySummary response model

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental sbom_service` — service tests pass

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:0dd83aa8d59effb7721bde3257c7efdda9b5370833f94ee121eeea24d9a282e1
