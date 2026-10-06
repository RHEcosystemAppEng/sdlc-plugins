# Bug Parsing: ACME-510

## Issue Metadata

- **Key**: ACME-510
- **Summary**: API response missing pagination headers when filtering by date range
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none)
- **Web URL**: https://mock-jira.example.com/browse/ACME-510

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

| Section | Present | Notes |
|---------|---------|-------|
| Issue Description | Yes | Clear description of the pagination header issue |
| Steps to Reproduce | Yes | 3 concrete steps |
| Expected Result | Yes | Specifies expected headers |
| Actual Result | Yes | Confirms body is correct but headers are missing |
| Environment / Version | Yes | Product version: 0.9.0, OS: RHEL 9.2, Deployment: OpenShift 4.14 |
| Attachments | Yes | None provided |

No optional sections (Root Cause, Suggested Fix) are present.
