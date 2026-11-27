Summary: Document advisory-summary endpoint in REST API reference
Epic: TC-9001: Documentation and feature validation
Labels: ai-generated-jira | Priority: Major | Fix Version: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference to cover the new endpoint introduced by TC-9001
(Add advisory severity aggregation endpoint).

What changed: a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns unique
advisory counts per severity for an SBOM as `{ critical, high, medium, low, total }`,
returns 404 for unknown SBOM IDs, is cached for 5 minutes (invalidated on advisory/SBOM
ingestion), and supports an optional `?threshold=<severity>` query parameter that limits
counts to severities at or above the threshold.

Doc impact type: **Updates** — add endpoint to REST API reference.

Details from Documentation Considerations:
- User purpose: API consumers need to know the endpoint path, parameters, and response shape.
- Reference material: existing SBOM advisory endpoints documentation.

Reference: Feature TC-9001.

## Acceptance Criteria
- [ ] REST API reference includes `GET /api/v2/sbom/{id}/advisory-summary` with path parameter, `threshold` query parameter (allowed values and semantics), and response shape
- [ ] 404 behavior for unknown SBOMs and 400 behavior for invalid `threshold` are documented
- [ ] Caching behavior (5-minute TTL, invalidation on ingestion) is documented
- [ ] Deduplication semantics (unique advisories by ID) are stated
- [ ] Documentation is placed alongside and consistent with the existing SBOM advisory endpoint documentation

## Test Requirements
- [ ] Verify documented path, parameters, status codes, and response fields match the implemented behavior (e.g., by calling the endpoint against a test instance)
- [ ] Verify example request/response in the docs are accurate and copy-paste runnable
- [ ] Verify documentation is complete for both MVP behavior and the `threshold` parameter

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory and SBOM ingestion
- Depends on: Task 4 — Support optional ?threshold query parameter on advisory-summary
