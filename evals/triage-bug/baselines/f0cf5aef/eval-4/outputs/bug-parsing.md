# Step 1 -- Bug Parsing: ACME-510

## Configuration Validation (Step 0)

Extracted from CLAUDE.md (`claude-md-bug-config.md`):

| Field | Value |
|-------|-------|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration. Validation **passed**.

## Issue Type Validation

- Issue ACME-510 has issue type Bug with ID **10020**
- Bug Configuration specifies Bug issue type ID **10020**
- **Match confirmed.** Issue type validation passed.

## Metadata

| Field | Value |
|-------|-------|
| Issue key | ACME-510 |
| Web URL | https://mock-jira.example.com/browse/ACME-510 |
| Summary | API response missing pagination headers when filtering by date range |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none) -- field is not populated |

## Bug Template Heading Formats

The bug description template at `docs/templates/bug-template.md` defines the following heading formats:

**Required Sections:**

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Environment / Version | `### **Environment / Version**` |
| Attachments | `### **Attachments**` |

**Optional Sections:**

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

## Parsed Required Sections

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

- Product version: 0.9.0
- OS: RHEL 9.2
- Deployment: OpenShift 4.14

### Attachments

None.

## Parsed Optional Sections

- **Root Cause**: Not present in bug description.
- **Suggested Fix**: Not present in bug description.

## Section Completeness

All required sections (Description, Steps to Reproduce, Expected Result, Actual Result, Environment / Version, Attachments) are present and populated.
Template conformance: **PASS**.
