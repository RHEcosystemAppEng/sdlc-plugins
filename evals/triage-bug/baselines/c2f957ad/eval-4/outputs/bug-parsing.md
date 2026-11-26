# Step 1 – Bug Parsing: ACME-510

## Step 0 – Configuration validation (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Rust backend service), Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | present ("No Serena MCP servers are configured") | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (mock: bug-template-mock.md) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete; proceed.

Note: the Registry lists Serena instance `serena_backend`, but Code Intelligence says no Serena servers are configured. The Read/Grep/Glob fallback applies.

## Issue type validation

- Issue type: Bug (ID: 10020)
- Configured Bug issue type ID: 10020
- Result: **match**. Proceed.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-510 |
| Web URL | https://mock-jira.example.com/browse/ACME-510 |
| Summary | API response missing pagination headers when filtering by date range |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none). `affectsVersions` is **not populated**, so Step 4.5.1 (keep/replace/augment) is skipped and Step 4.5 starts at 4.5.2 |

## Parsed sections (headings matched against the bug template)

### Required sections

| Section | Template heading | Found |
|---|---|---|
| Description | `### **Issue Description**` | yes |
| Steps to reproduce | `### **Steps to Reproduce**` | yes |
| Expected Result | `### **Expected Result**` | yes |
| Actual Result | `### **Actual Result**` | yes |
| Environment / Version | `### **Environment / Version**` | yes |
| Attachments | `### **Attachments**` | yes ("None.") |

All required sections are present. No missing-section stop.

#### Description
When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters, the response is missing the `X-Total-Count` and `Link` pagination headers. The response body contains the correct filtered results, but clients relying on pagination headers cannot determine total pages.

#### Steps to Reproduce
1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

#### Expected Result
The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

#### Actual Result
The response body contains the correct filtered advisories, but the `X-Total-Count` and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`) return pagination headers correctly.

#### Environment / Version
```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```
- Extracted product version: **0.9.0**
- OS: RHEL 9.2
- Deployment: OpenShift 4.14

#### Attachments
None.

### Optional sections

| Section | Present |
|---|---|
| Root Cause | no |
| Suggested Fix | no |

### Observations
- The Description names the query parameter as `filterDateRange`. The Steps to Reproduce use `publishedAfter` / `publishedBefore`. The two most likely refer to the same date-range filter feature, but the investigation should confirm which parameter names the endpoint actually accepts.
- The Component is `sdlc-workflow`, but the bug describes a backend REST endpoint in acme-backend. The Component field doesn't match the affected code, so the target repository is chosen from the code paths in the description (acme-backend).
