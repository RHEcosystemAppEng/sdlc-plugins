# Task 5 — Document the advisory-summary endpoint in the REST API reference

**Summary:** TC-9001: Document GET /api/v2/sbom/{id}/advisory-summary in the REST API reference
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9001)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Feature TC-9001 adds a new REST endpoint, `GET /api/v2/sbom/{id}/advisory-summary`. It returns the number of unique vulnerability advisories affecting an SBOM at each severity level (`{ critical, high, medium, low, total }`), returns 404 for unknown SBOM IDs, and caches responses for 5 minutes. Cached summaries are invalidated when new advisories are linked to the SBOM. It also accepts an optional `?threshold=<severity>` query parameter that limits the counts to severities at or above the threshold.

**Doc impact type:** Updates (to existing content). Add the endpoint to the REST API reference.

**Details from Documentation Considerations:**
- User purpose: API consumers need to know the endpoint path, parameters, and response shape.
- Reference material: the existing SBOM advisory endpoint documentation (`GET /api/v2/sbom/{id}/advisories`). Match its structure and style.

Reference: TC-9001 (Add advisory severity aggregation endpoint).

## Acceptance Criteria
- [ ] The REST API reference has an entry for `GET /api/v2/sbom/{id}/advisory-summary`, placed with the existing SBOM advisory endpoint docs
- [ ] The entry documents the path parameter `id`, the optional `threshold` query parameter (allowed values: `critical`, `high`, `medium`, `low`) and its at-or-above semantics
- [ ] The entry documents the 200 response shape `{ critical, high, medium, low, total }` and states that counts are deduplicated by advisory ID
- [ ] The entry documents the 404 response for an unknown SBOM ID and the 400 response for an invalid `threshold`
- [ ] The entry notes the 5-minute response caching and that summaries are refreshed when new advisories are correlated
- [ ] Documentation style and structure match the existing SBOM advisory endpoint documentation

## Test Requirements
- [ ] Check each documented field, status code, and parameter against the merged implementation (Tasks 1–4) by calling the running endpoint
- [ ] Confirm the example request/response in the docs can be reproduced against a test instance
- [ ] Confirm the docs match the implemented threshold semantics (omitted vs zeroed buckets) as finally agreed on TC-9001

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and SbomService aggregation query
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling and 5-minute caching
- Depends on: Task 3 — Invalidate cached SBOM advisory summaries from the ingestion pipeline
- Depends on: Task 4 — Add optional ?threshold= severity filter to GET /api/v2/sbom/{id}/advisory-summary
