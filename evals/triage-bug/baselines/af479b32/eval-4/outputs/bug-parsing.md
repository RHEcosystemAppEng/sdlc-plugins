# Step 1 -- Bug Parsing: ACME-510

## Metadata

- **Issue Key**: ACME-510
- **Web URL**: https://mock-jira.example.com/browse/ACME-510
- **Summary**: API response missing pagination headers when filtering by date range
- **Issue Type**: Bug (ID: 10020) -- matches Bug Configuration (validated)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is not populated

## Parsed Description Sections

### Required Sections

All required sections from the bug template (`docs/templates/bug-template.md`) are present.

#### Issue Description (`### **Issue Description**`)

When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters,
the response is missing the `X-Total-Count` and `Link` pagination headers. The response
body contains the correct filtered results, but clients relying on pagination headers
cannot determine total pages.

#### Steps to Reproduce (`### **Steps to Reproduce**`)

1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

#### Expected Result (`### **Expected Result**`)

The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

#### Actual Result (`### **Actual Result**`)

The response body contains the correct filtered advisories, but the `X-Total-Count`
and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`)
return pagination headers correctly.

#### Environment / Version (`### **Environment / Version**`)

- Product version: 0.9.0
- OS: RHEL 9.2
- Deployment: OpenShift 4.14

#### Attachments (`### **Attachments**`)

None.

### Optional Sections

- **Root Cause**: Not present in the bug description.
- **Suggested Fix**: Not present in the bug description.

## Validation Result

All required sections are present and well-formed. Proceeding with investigation.
