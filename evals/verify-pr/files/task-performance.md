<!-- SYNTHETIC TEST DATA — mock Jira task description for eval testing; names, URLs, and identifiers are fictional -->

# Jira Task: TC-9107

**Key**: TC-9107
**Summary**: Batch advisory queries in SBOM detail endpoint to eliminate N+1
**Status**: In Review
**Labels**: ai-generated-jira, performance-optimization, backend, query-optimization
**PR URL**: https://github.com/trustify/trustify-backend/pull/801
**Web URL**: https://redhat.atlassian.net/browse/TC-9107
**Parent Feature**: TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Replace the sequential per-advisory query loop in the SBOM detail endpoint with a single
batched query. Currently, `SbomService::fetch_details` loads the SBOM, then iterates over
linked advisories calling `AdvisoryService::fetch` individually for each one. With SBOMs
linked to 200+ advisories, this produces ~200 sequential DB queries and pushes response
time above the 200ms target.

**Implementation approach:**

1. Add a `fetch_advisories_batch` method to `AdvisoryService` that accepts `Vec<Uuid>`
   and returns all matching advisories in a single `WHERE id IN (...)` query.
2. Update `SbomService::fetch_details` to collect advisory IDs first, then call the
   batch method once instead of looping.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — add `fetch_advisories_batch` method
- `modules/fundamental/src/sbom/service/sbom.rs` — replace per-advisory loop with batch call

## Files to Create
- `tests/api/sbom_advisory_batch.rs` — integration test verifying batch loading produces same results

## Implementation Notes
- Follow the existing `fetch` method pattern in `advisory/service/advisory.rs` for the batch variant
- Use SeaORM's `.is_in()` filter for the batch query (see `common/src/db/query.rs` for examples)
- The `sbom_advisory` join table in `entity/src/sbom_advisory.rs` links SBOMs to advisories
- Error handling: return `AppError` with `.context()` wrapping, matching existing patterns
- Ensure the batch method preserves the same `AdvisoryDetails` response shape as the individual `fetch`

## Acceptance Criteria
- [ ] SBOM detail endpoint returns identical advisory data as before (no behavioral change)
- [ ] Response time for SBOMs with 200+ advisories is under 200ms p95
- [ ] All existing SBOM and advisory endpoint tests pass
- [ ] No increase in error rate

## Test Requirements
- [ ] Test that batch loading returns the same advisory details as individual loading
- [ ] Test that an SBOM with no advisories returns an empty list (not an error)
- [ ] Test that duplicate advisory IDs are handled gracefully

## Baseline Metrics
- **Response Time (p95):** 850ms (`GET /api/v2/sbom/{id}` with 200+ advisories)
- **Queries per request:** ~200 sequential

## Target Metrics
- **Response Time (p95):** < 200ms
- **Queries per request:** < 5

## Performance Test Requirements
- [ ] Run performance baseline after implementation
- [ ] Verify SBOM detail response time is under 200ms p95 for 200+ advisory SBOMs
- [ ] Compare against baseline metrics and confirm improvement
