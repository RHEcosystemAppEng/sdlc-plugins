# Task 8: Add API reference documentation for remediation endpoints

Parent Epic: TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
main

## Description
Add API reference documentation for the new remediation aggregation endpoints. Document the request/response formats, query parameters, and example responses for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`. This task addresses the "New Content" documentation consideration from the feature specification.

## Files to Modify
- `README.md` — add a "Remediation API" section documenting the two new endpoints with request/response schemas and example usage

## Implementation Notes
- Document `GET /api/v2/remediation/summary` with: endpoint URL, HTTP method, description, response schema (JSON with `counts` array of `{severity, status, count}` objects), and example response body.
- Document `GET /api/v2/remediation/by-product` with: endpoint URL, HTTP method, description, query parameters (`offset`, `limit`, `product_name`), response schema (paginated `{items: [{productName, total, open, inProgress, resolved}], total, offset, limit}`), and example response body.
- Follow the existing documentation structure in `README.md` — reference how other endpoints (SBOM, advisory) are documented, if present.
- Include a note about the p95 < 500ms performance target for the summary endpoint.
- Mention that no new database tables are required — aggregations are computed from existing SBOM, advisory, and vulnerability data.

## Acceptance Criteria
- [ ] `README.md` contains a "Remediation API" section with documentation for both endpoints
- [ ] `GET /api/v2/remediation/summary` documentation includes endpoint URL, response schema, and example response
- [ ] `GET /api/v2/remediation/by-product` documentation includes endpoint URL, query parameters, response schema, and example response
- [ ] Documentation mentions the p95 < 500ms performance target

## Documentation Updates
- `README.md` — add "Remediation API" section with endpoint reference for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints
