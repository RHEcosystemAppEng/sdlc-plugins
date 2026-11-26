# Step 1 – Fetch Bug: Parsed Description (ACME-510)

## Step 0 – Configuration validation (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Rust backend service), Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present; states no Serena MCP servers are configured | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (eval: bug-template-mock.md) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete, so triage continues.

## Issue type validation

- Issue `issuetype.id` = **10020**
- Configured Bug issue type ID = **10020**
- **Match**, so this is a Bug and triage continues.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-510 |
| Web URL | https://mock-jira.example.com/browse/ACME-510 |
| Summary | API response missing pagination headers when filtering by date range |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none). The `versions` field is **not populated**, so Step 4.5.1 (keep/replace/augment) is skipped and Step 4.5 runs from 4.5.2 |

## Required Sections (heading formats from the bug template)

All required sections are present.

### Description (`### **Issue Description**`)

When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters,
the response is missing the `X-Total-Count` and `Link` pagination headers. The response
body contains the correct filtered results, but clients relying on pagination headers
cannot determine total pages.

### Steps to Reproduce (`### **Steps to Reproduce**`)

1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

### Expected Result (`### **Expected Result**`)

The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

### Actual Result (`### **Actual Result**`)

The response body contains the correct filtered advisories, but the `X-Total-Count`
and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`)
return pagination headers correctly.

### Environment / Version (`### **Environment / Version**`)

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

- Product version: **0.9.0**. This is the version candidate for Step 4.5.
- OS: RHEL 9.2 (an environment detail, not a product version)
- Deployment: OpenShift 4.14 (a platform version, not a product version)

### Attachments (`### **Attachments**`)

None.

## Optional Sections

| Section | Present? | Content |
|---|---|---|
| Root Cause (`### **Root Cause**`) | No | none |
| Suggested Fix (`### **Suggested Fix**`) | No | none |

## Parsing notes

- The Description names the parameter as `filterDateRange`, but the Steps to Reproduce
  use `publishedAfter` / `publishedBefore`. These are taken to mean the same date-range
  filter. The reproducer should use the concrete parameters from the Steps to Reproduce.
- The Component is `sdlc-workflow`, which does not fit an `/api/v2/advisories` REST
  endpoint bug. The target repository is therefore chosen from the code paths in the
  description: the endpoint belongs to the Rust backend, `acme-backend`.
