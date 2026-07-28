<!-- SYNTHETIC TEST DATA — bug issue with version info in Environment/Version section for triage-bug Affects Version eval testing -->

# Mock Jira Bug Issue

**Key**: ACME-510
**Summary**: API response missing pagination headers when filtering by date range
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Affects Version/s**: (none)
**Web URL**: https://mock-jira.example.com/browse/ACME-510

**Available Jira Versions**:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

---

## Description

### **Issue Description**

When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters,
the response is missing the `X-Total-Count` and `Link` pagination headers. The response
body contains the correct filtered results, but clients relying on pagination headers
cannot determine total pages.

### **Steps to Reproduce**

1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

### **Expected Result**

The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

### **Actual Result**

The response body contains the correct filtered advisories, but the `X-Total-Count`
and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`)
return pagination headers correctly.

### **Environment / Version**

Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14

### **Attachments**

None.
