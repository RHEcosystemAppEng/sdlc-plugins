# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-510)

## Step 0 — Configuration validation

Source: `claude-md-bug-config.md` (project CLAUDE.md)

| Check | Result |
|---|---|
| Repository Registry | Present — 1 entry: `acme-backend` (Rust backend service, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`) |
| Jira Configuration | Present — Project key `ACME`, Cloud ID `mock-cloud-id-for-eval` |
| Code Intelligence | Present — says no Serena MCP servers are configured (conflicts with the Registry, which names `serena_backend`). Treated as "Serena unavailable", so investigation falls back to Read/Grep/Glob |
| Bug Configuration | Present — Bug issue type ID `10020`, Bug template path `docs/templates/bug-template.md` (eval mock: `bug-template-mock.md`), Bug-to-Task link type `Blocks` |

Result: **PASS**. Execution continues.

## Step 0.5 — Jira access

This is an eval, so no Jira MCP or REST calls were made. Bug data comes from `bug-issue-with-version.md`.

## Step 1 — Fetch Bug

### Issue type validation

- Issue type: Bug (ID `10020`)
- Configured Bug issue type ID: `10020`
- Result: **MATCH**. Execution continues.

### Metadata

| Field | Value |
|---|---|
| Key | ACME-510 |
| Summary | API response missing pagination headers when filtering by date range |
| Status | New |
| Labels | `reported-by-user` |
| Component | `sdlc-workflow` (does not match the affected code, which is the `/api/v2/advisories` backend endpoint. Target repo is chosen from the endpoint, not the Component field) |
| Affects Version/s | (none). `affectsVersions` is **not populated**, so Step 4.5.1 (keep/replace/augment) is skipped |
| Web URL | https://mock-jira.example.com/browse/ACME-510 |

### Template heading formats (from bug-template-mock.md)

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`, `### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

### Parsed Required Sections

#### Description (`### **Issue Description**`)
When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters, the response is missing the `X-Total-Count` and `Link` pagination headers. The response body contains the correct filtered results, but clients relying on pagination headers cannot determine total pages.

#### Steps to Reproduce (`### **Steps to Reproduce**`)
1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

#### Expected Result (`### **Expected Result**`)
The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

#### Actual Result (`### **Actual Result**`)
The response body contains the correct filtered advisories, but the `X-Total-Count` and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`) return pagination headers correctly.

#### Environment / Version (`### **Environment / Version**`)
```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```
- Product version: **0.9.0** (passed to Step 4.5 for Affects Version resolution)
- OS: RHEL 9.2
- Deployment: OpenShift 4.14

#### Attachments (`### **Attachments**`)
None.

### Optional Sections

| Section | Present? | Content |
|---|---|---|
| Root Cause | No | — |
| Suggested Fix | No | — |

### Completeness check

All 6 required sections are present. **No missing sections.** Triage continues.

### Note on wording

The Description says "`filterDateRange` query parameters", but the reproducer uses `publishedAfter` / `publishedBefore`. Investigation treats `publishedAfter`/`publishedBefore` as the real parameters and `filterDateRange` as the reporter's name for them, or possibly the name of an internal filter type.
