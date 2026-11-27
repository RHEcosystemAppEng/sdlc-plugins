# Step 1 – Bug Parsing: ACME-511

## Step 0 – Configuration validation (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Serena: serena_backend, Path: /home/dev/repos/acme-backend) | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present ("No Serena MCP servers are configured") | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (mocked by bug-template-mock.md) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete. Proceeding.

## Issue type validation

- Issue type ID on ACME-511: **10020**
- Configured Bug issue type ID: **10020**
- Result: **match** — issue is a Bug.

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

## Parsed description sections (matched against template headings)

### Required sections

| Section | Template heading | Found |
|---|---|---|
| Description | `### **Issue Description**` | yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | yes |
| Expected Result | `### **Expected Result**` | yes |
| Actual Result | `### **Actual Result**` | yes |
| Environment / Version | `### **Environment / Version**` | yes (content is vague — no version identifier) |
| Attachments | `### **Attachments**` | yes ("None.") |

All required sections are present; no missing-section stop condition.

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

Note: the section is present but contains **no version identifier** (no explicit
version number, no product-prefixed version, no "version X.Y.Z" pattern). Only a
vague environment reference ("staging"). This is carried into Step 4.5.

#### Attachments
None.

### Optional sections

| Section | Found |
|---|---|
| Root Cause | no |
| Suggested Fix | no |
