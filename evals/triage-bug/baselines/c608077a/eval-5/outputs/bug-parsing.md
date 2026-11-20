# Step 1 – Fetch Bug: ACME-511

## Step 0 – Configuration validation (from claude-md-bug-config.md)

| Check | Result |
|---|---|
| Repository Registry | Present: `acme-backend` (Rust backend service), Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | Project key `ACME`, Cloud ID `mock-cloud-id-for-eval` |
| Code Intelligence | Present (says no Serena MCP servers are configured) |
| Bug Configuration | Bug issue type ID `10020`; Bug template path `docs/templates/bug-template.md` (mocked by bug-template-mock.md); Bug-to-Task link type `Blocks` |

Configuration is complete, so we continue.

## Issue type validation

- Issue type on ACME-511: Bug (ID `10020`)
- Configured Bug issue type ID: `10020`
- Result: **match**. Continue.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-511 |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none). **`affectsVersions` is NOT populated**, so Step 4.5.1 (keep/replace/augment) does not apply and Step 4.5 starts at 4.5.2. |

## Parsed description sections

Headings matched against the template's Required/Optional Sections tables.

### Required sections

| Section | Template heading | Found | Content |
|---|---|---|---|
| Description | `### **Issue Description**` | Yes | When a user enables dark mode via the settings panel and then closes and reopens the browser, the application reverts to light mode. The preference is not persisted. |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes | 1. Open the application in a browser. 2. Navigate to Settings > Appearance. 3. Toggle "Dark Mode" to ON. 4. Close the browser completely. 5. Reopen the browser and navigate back to the application. |
| Expected Result | `### **Expected Result**` | Yes | The application should load in dark mode, matching the user's last preference. |
| Actual Result | `### **Actual Result**` | Yes | The application loads in light mode. The dark mode toggle is reset to OFF. |
| Environment / Version | `### **Environment / Version**` | Yes | "Not sure which version — using whatever is deployed on staging." |
| Attachments | `### **Attachments**` | Yes | None. |

### Environment / Version (verbatim)

> Not sure which version — using whatever is deployed on staging.

The section exists, so it passes the required-section check. Its content is vague: it gives no version number, no product-prefixed version, and no "version X.Y.Z" phrase. The only environment detail is "staging", and staging is a deployment target, not a release. Step 4.5.2 handles this (see version-resolution.md).

### Optional sections

| Section | Template heading | Found |
|---|---|---|
| Root Cause | `### **Root Cause**` | No. The reporter gave no prior analysis. |
| Suggested Fix | `### **Suggested Fix**` | No |

## Completeness verdict

All required sections are present, so the bug report is complete. Triage continues to Step 2.
