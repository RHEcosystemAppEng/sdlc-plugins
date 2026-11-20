## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation for the new advisory severity aggregation endpoint introduced by TC-9001.

**What changed:** a new endpoint, `GET /api/v2/sbom/{id}/advisory-summary`, returns unique-advisory severity counts `{ critical, high, medium, low, total }` for an SBOM. It returns 404 for an unknown SBOM ID, responses are cached for 5 minutes (invalidated when new advisories are linked), and it supports an optional `?threshold=<severity>` query parameter that returns only counts at or above that severity.

**Doc impact type:** Updates — add the endpoint to the REST API reference.

**Details from Documentation Considerations:**
- User purpose: API consumers need to know the endpoint path, parameters, and response shape.
- Reference material: existing SBOM advisory endpoints documentation (e.g., `GET /api/v2/sbom/{id}/advisories`).

Feature reference: TC-9001.

## Acceptance Criteria
- [ ] The REST API reference documents `GET /api/v2/sbom/{id}/advisory-summary` with path, `id` parameter, optional `threshold` parameter (allowed values), and response shape
- [ ] The 404 behavior for an unknown SBOM and the 5-minute caching/invalidation behavior are documented
- [ ] Deduplication semantics (counts are of unique advisories) are stated
- [ ] Documentation style matches the existing SBOM advisory endpoint documentation

## Test Requirements
- [ ] Verify the documented path, parameters, and response fields match the implemented endpoint (compare against a live response)
- [ ] Verify the documented example requests/responses are accurate
- [ ] Verify the threshold examples match the implemented filter behavior

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Add optional threshold query parameter to advisory-summary endpoint
