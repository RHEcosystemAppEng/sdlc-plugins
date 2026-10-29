# Step 1 -- Bug Parsing: ACME-510

## Metadata

- **Issue Key**: ACME-510
- **Web URL**: https://mock-jira.example.com/browse/ACME-510
- **Summary**: API response missing pagination headers when filtering by date range
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is empty / not populated

## Configuration Validation (Step 0)

Extracted from CLAUDE.md Bug Configuration:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Issue type validation: Issue type ID 10020 matches Bug issue type ID 10020 from Bug Configuration. Validated.

## Bug Template Sections

Template file defines the following heading formats:

### Required Sections

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Environment / Version | `### **Environment / Version**` |
| Attachments | `### **Attachments**` |

### Optional Sections

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

## Parsed Description Sections

### Issue Description (Required -- PRESENT)

When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters,
the response is missing the `X-Total-Count` and `Link` pagination headers. The response
body contains the correct filtered results, but clients relying on pagination headers
cannot determine total pages.

### Steps to Reproduce (Required -- PRESENT)

1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

### Expected Result (Required -- PRESENT)

The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

### Actual Result (Required -- PRESENT)

The response body contains the correct filtered advisories, but the `X-Total-Count`
and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`)
return pagination headers correctly.

### Environment / Version (Required -- PRESENT)

Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14

### Attachments (Required -- PRESENT)

None.

### Root Cause (Optional -- NOT PRESENT)

Not provided by reporter.

### Suggested Fix (Optional -- NOT PRESENT)

Not provided by reporter.

## Parsing Result

All 6 required sections are present. Bug description conforms to the template at `docs/templates/bug-template.md`. Proceeding with triage.
