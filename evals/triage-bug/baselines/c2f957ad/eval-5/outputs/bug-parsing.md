# Step 0 / Step 1 – Configuration Validation and Bug Parsing: ACME-511

## Step 0 – Project Configuration (from claude-md-bug-config.md)

| Section | Present | Extracted values |
|---|---|---|
| Repository Registry | Yes | acme-backend (Rust backend service), Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | Yes | Project key: `ACME`, Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Yes | No Serena MCP servers configured; fall back to Read/Grep/Glob |
| Bug Configuration | Yes | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md` (mocked by bug-template-mock.md); Bug-to-Task link type: `Blocks` |

Result: configuration is complete. Proceed.

## Step 1 – Issue Type Validation

- Issue type on ACME-511: Bug (ID `10020`)
- Configured Bug issue type ID: `10020`
- Result: **match**. Proceed.

## Step 1 – Metadata

| Field | Value |
|---|---|
| Issue key | ACME-511 |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none) |
| affectsVersions populated? | **No** (empty) -> Step 4.5.1 does not apply; Step 4.5.2 must extract from description |

## Step 1 – Parsed Description Sections

Headings matched against the template's Required/Optional Sections tables.

### Required Sections

| Section | Template heading | Found | Content |
|---|---|---|---|
| Description | `### **Issue Description**` | Yes | When a user enables dark mode via the settings panel and then closes and reopens the browser, the application reverts to light mode. The preference is not persisted. |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes | 1. Open the application in a browser. 2. Navigate to Settings > Appearance. 3. Toggle "Dark Mode" to ON. 4. Close the browser completely. 5. Reopen the browser and navigate back to the application. |
| Expected Result | `### **Expected Result**` | Yes | The application should load in dark mode, matching the user's last preference. |
| Actual Result | `### **Actual Result**` | Yes | The application loads in light mode. The dark mode toggle is reset to OFF. |
| Environment / Version | `### **Environment / Version**` | Yes | "Not sure which version — using whatever is deployed on staging." |
| Attachments | `### **Attachments**` | Yes | None. |

### Optional Sections

| Section | Template heading | Found | Content |
|---|---|---|---|
| Root Cause | `### **Root Cause**` | No | — |
| Suggested Fix | `### **Suggested Fix**` | No | — |

### Completeness check

All required sections are present. The Environment / Version section is present but its
content is vague: it contains no version identifier (only "Not sure which version" and
"whatever is deployed on staging"). This does not block triage (the section exists), but
it means Affects Version cannot be derived in Step 4.5 — see version-resolution.md.
