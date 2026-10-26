# Bug Parsing - ACME-510

## Issue Metadata

- **Key**: ACME-510
- **Summary**: API response missing pagination headers when filtering by date range
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none)

## Parsed Description Sections

### Issue Description

When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters,
the response is missing the `X-Total-Count` and `Link` pagination headers. The response
body contains the correct filtered results, but clients relying on pagination headers
cannot determine total pages.

### Steps to Reproduce

1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

### Expected Result

The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

### Actual Result

The response body contains the correct filtered advisories, but the `X-Total-Count`
and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`)
return pagination headers correctly.

### Environment / Version

Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14

### Attachments

None.

## Template Conformance

All required sections from the bug template are present:

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Environment / Version | Present |
| Attachments | Present |

No optional sections (Root Cause, Suggested Fix) are included.
