# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns
per-severity counts (Critical, High, Medium, Low) and a total for a given SBOM.

**Jira Issue**: TC-9201
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model sub-module. Follows the
existing pattern where `mod.rs` declares `pub mod summary;` and `pub mod details;`.

### 2. `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`. The method:
- Takes `&self, sbom_id: Id, tx: &Transactional<'_>`
- Queries the `sbom_advisory` join table to find advisories linked to the SBOM
- Joins with advisory data to get severity for each advisory
- Deduplicates by advisory ID
- Counts advisories per severity level (Critical, High, Medium, Low)
- Returns `Result<SeveritySummary, AppError>`
- Returns 404 via `AppError` if the SBOM ID does not exist

### 3. `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route:
```rust
Router::new().route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
```
Follows the existing `Router::new().route(...)` pattern used for other advisory endpoints.

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`

New response struct `SeveritySummary` with fields:
- `critical: u64`
- `high: u64`
- `medium: u64`
- `low: u64`
- `total: u64`

Derives: `Debug, Clone, Serialize, Deserialize, Default, PartialEq, Eq`

All fields default to 0 when no advisories exist at that level (via `Default` derive).

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

GET handler function for `/api/v2/sbom/{id}/advisory-summary`:
- Extracts `sbom_id` via `Path<Id>`
- Calls `AdvisoryService::severity_summary(sbom_id, &tx)`
- Returns `Json<SeveritySummary>` on success
- Returns `AppError` with `.context()` on failure
- Follows the pattern in `modules/fundamental/src/advisory/endpoints/get.rs`

### 6. `tests/api/advisory_summary.rs`

Integration tests covering all test requirements:
1. Valid SBOM with known advisories returns correct severity counts
2. Non-existent SBOM ID returns 404
3. SBOM with no advisories returns all zeros
4. Duplicate advisory links are deduplicated in the count

Each test has a doc comment and given-when-then structure.

## Data Flow Trace

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary`
2. **Extraction**: Axum `Path<Id>` extracts `sbom_id` from URL
3. **Service call**: Handler calls `AdvisoryService::severity_summary(sbom_id, &tx)`
4. **Database query**: Service queries `sbom_advisory` join table filtered by `sbom_id`,
   joins with `advisory` table to get severity, deduplicates by advisory ID
5. **Aggregation**: Counts per severity level, computes total
6. **Response**: Returns `SeveritySummary` struct serialized as JSON via `Json` extractor
7. **Error path**: If SBOM not found, returns 404 via `AppError`

All stages are connected; no missing or disconnected stages.

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns per-severity
counts (critical, high, medium, low) and total for advisories linked
to a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201
```

With trailer: `Assisted-by: Claude Code`

## Verification Checklist

- [ ] `SeveritySummary` struct created with all five fields defaulting to 0
- [ ] `severity_summary` service method queries `sbom_advisory`, deduplicates, counts by severity
- [ ] Route registered in `endpoints/mod.rs`
- [ ] Model module registered in `model/mod.rs`
- [ ] 404 returned for non-existent SBOM ID
- [ ] All four integration tests pass
- [ ] Response time acceptable for up to 500 advisories (single query with GROUP BY)
- [ ] No out-of-scope file modifications
- [ ] `cargo test -p trustify-fundamental` passes
- [ ] No sensitive patterns in diff
