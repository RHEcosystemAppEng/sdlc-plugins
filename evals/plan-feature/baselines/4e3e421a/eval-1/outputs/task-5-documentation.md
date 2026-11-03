## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation for the new advisory severity aggregation endpoint introduced by Feature TC-9001.

**What changed:** A new endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns aggregated vulnerability advisory severity counts for an SBOM as `{ critical, high, medium, low, total }`. Counts include only unique advisories, deduplicated by advisory ID. The endpoint returns 404 when the SBOM does not exist and caches responses for 5 minutes, with invalidation when new advisories are linked to the SBOM. An optional non-MVP `?threshold=<severity>` query parameter filters the counts to severities at or above the given level. Document it only if Task 4 ships in the same release.

**Doc impact type:** Updates (to existing content)

**Details from Documentation Considerations:**
- Add the endpoint to the REST API reference
- User purpose: API consumers need to know the endpoint path, parameters, and response shape
- Reference material: the existing SBOM advisory endpoint documentation (for example, `GET /api/v2/sbom/{id}/advisories`)

Feature reference: TC-9001

## Acceptance Criteria
- [ ] The REST API reference includes `GET /api/v2/sbom/{id}/advisory-summary`, with its path parameter, response shape, and example response
- [ ] The 404 behavior for a non-existent SBOM is documented
- [ ] Deduplication semantics ("unique advisories by advisory ID") are documented
- [ ] Caching behavior (5-minute cache, invalidated on advisory ingestion) is documented
- [ ] If Task 4 shipped, the `threshold` parameter is documented with its valid values and the 400 response for invalid values
- [ ] Formatting and structure match the existing SBOM advisory endpoint documentation

## Test Requirements
- [ ] Every documented field name and status code matches the implemented endpoint, verified against a running instance or the integration tests
- [ ] The example request and response in the docs can be reproduced against a test deployment
- [ ] Documentation is complete for the scope listed in Documentation Considerations

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Add optional threshold query parameter (only if it ships in the same release)
