# Step 1 – Fetch Bug: Parsed Description (ACME-511)

## Step 0 – Configuration validation (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Rust backend service), Serena: serena_backend, Path: /home/dev/repos/acme-backend | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present; "No Serena MCP servers are configured" | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (eval: bug-template-mock.md) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete — proceed.

## Issue type validation

- Issue `issuetype.id`: 10020 (Bug)
- Configured Bug issue type ID: 10020
- Result: **match** — proceed with triage.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-511 |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none) — `versions` field is **not populated** (Step 4.5.1 will not prompt keep/replace/augment) |

## Parsed sections (heading formats from bug template)

### Required Sections

| Section | Template heading | Found? |
|---|---|---|
| Description | `### **Issue Description**` | yes |
| Steps to reproduce | `### **Steps to Reproduce**` | yes |
| Expected Result | `### **Expected Result**` | yes |
| Actual Result | `### **Actual Result**` | yes |
| Environment / Version | `### **Environment / Version**` | yes (present, but contains no version identifier) |
| Attachments | `### **Attachments**` | yes |

#### Description
When a user enables dark mode via the settings panel and then closes and reopens the
browser, the application reverts to light mode. The preference is not persisted.

#### Steps to Reproduce
1. Open the application in a browser.
2. Navigate to Settings > Appearance.
3. Toggle "Dark Mode" to ON.
4. Close the browser completely.
5. Reopen the browser and navigate back to the application.

#### Expected Result
The application should load in dark mode, matching the user's last preference.

#### Actual Result
The application loads in light mode. The dark mode toggle is reset to OFF.

#### Environment / Version
> Not sure which version — using whatever is deployed on staging.

Parsing note: the section heading exists, so it satisfies the required-section check,
but its content is vague. It contains no explicit version number (e.g. `1.2.3`), no
product-prefixed version (e.g. `ACME 2.1.0`), and no "version N.N.N" pattern. The only
environment hint is "staging". This is carried forward to Step 4.5.

#### Attachments
None.

### Optional Sections

| Section | Found? |
|---|---|
| Root Cause | not present |
| Suggested Fix | not present |

## Completeness result

All required sections are present. No missing sections — triage continues.
