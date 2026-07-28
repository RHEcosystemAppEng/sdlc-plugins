# Bug Parsing – ACME-510 (Step 1)

## Configuration Validation

- Project key: ACME
- Cloud ID: mock-cloud-id-for-eval
- Bug issue type ID: 10020
- Bug template path: docs/templates/bug-template.md
- Bug-to-Task link type: Blocks

## Issue Type Validation

- Issue's `issuetype.id`: 10020
- Bug Configuration `Bug issue type ID`: 10020
- Result: **MATCH** — proceeding with triage.

## Metadata

| Field             | Value                                                       |
|-------------------|-------------------------------------------------------------|
| Issue Key         | ACME-510                                                    |
| Web URL           | https://mock-jira.example.com/browse/ACME-510               |
| Summary           | API response missing pagination headers when filtering by date range |
| Issue Type        | Bug (ID: 10020)                                             |
| Status            | New                                                         |
| Labels            | reported-by-user                                            |
| Component         | sdlc-workflow                                               |
| Affects Version/s | (none — `affectsVersions` field is empty)                   |

## Required Sections (from bug-template.md)

All required sections are present. Parsed content follows.

---

### Description

> When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters,
> the response is missing the `X-Total-Count` and `Link` pagination headers. The response
> body contains the correct filtered results, but clients relying on pagination headers
> cannot determine total pages.

---

### Steps to Reproduce

1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

---

### Expected Result

The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

---

### Actual Result

The response body contains the correct filtered advisories, but the `X-Total-Count`
and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`)
return pagination headers correctly.

---

### Environment / Version

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

---

### Attachments

None.

---

## Optional Sections

| Section      | Present |
|--------------|---------|
| Root Cause   | No      |
| Suggested Fix | No     |

## Required Section Check

All five required sections defined in the bug template are present:
- `### **Issue Description**` ✓
- `### **Steps to Reproduce**` ✓
- `### **Expected Result**` ✓
- `### **Actual Result**` ✓
- `### **Environment / Version**` ✓

**No missing required sections — investigation may proceed.**

## Affects Version Status

The `affectsVersions` field is **empty** on this issue. Step 4.5 will extract a version
from the Environment / Version section and offer to set it.
