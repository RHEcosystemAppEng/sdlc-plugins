**Summary**: Document advisory-summary endpoint in REST API reference

## Repository
trustify-backend

## Target Branch
main

## Description
Feature TC-9001 adds `GET /api/v2/sbom/{id}/advisory-summary`, which returns unique-advisory severity counts `{ critical, high, medium, low, total }` for an SBOM, returns 404 for an unknown SBOM, caches responses for 5 minutes (invalidated when new advisories are linked via ingestion), and supports an optional `?threshold=<severity>` query parameter.

**Doc impact type**: Updates to existing content — add the endpoint to the REST API reference.

- **User purpose**: API consumers need to know the endpoint path, parameters, and response shape.
- **Reference material**: existing SBOM advisory endpoints documentation (e.g. `GET /api/v2/sbom/{id}/advisories`).

Document: path and method, `id` path parameter, optional `threshold` parameter (allowed values, inclusive semantics, 400 on invalid value), response schema and example, 404 behaviour, deduplication of advisories by ID, handling of advisories without a recognised severity, and caching/freshness behaviour (up to 5 minutes, invalidated on advisory ingestion).

## Acceptance Criteria
- [ ] The REST API reference includes `GET /api/v2/sbom/{id}/advisory-summary` next to the existing SBOM advisory endpoints
- [ ] Response shape, field meanings, and an example response are documented
- [ ] 404 behaviour for unknown SBOM IDs is documented
- [ ] The optional `threshold` parameter, its allowed values, semantics, and 400 error are documented
- [ ] Caching (5-minute TTL) and invalidation-on-ingestion behaviour are described

## Test Requirements
- [ ] Verify documented paths, parameters, status codes, and response field names match the implemented behaviour (Tasks 1–4) by exercising the endpoint
- [ ] Verify the example response is valid against the implemented `AdvisorySeveritySummary` schema
- [ ] Verify consistency in style and structure with the existing SBOM advisory endpoint docs

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and SBOM aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Support optional threshold query parameter on advisory-summary (non-MVP)
