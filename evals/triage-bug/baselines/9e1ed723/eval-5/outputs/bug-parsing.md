# Step 1 – Bug Parsing: ACME-511

## Step 0 – Configuration Validation (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Serena: serena_backend, Path: /home/dev/repos/acme-backend) | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present ("No Serena MCP servers are configured") | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (mocked by bug-template-mock.md) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete — proceed.

## Issue Type Validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **match** — issue is a Bug, triage continues.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-511 |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none) |
| `affectsVersions` already populated? | **No** — Step 4.5.1 will not prompt keep/replace/augment; proceed to extraction (4.5.2) |

## Template Heading Formats Used for Parsing

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`,
`### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

## Parsed Required Sections

### Description (`### **Issue Description**`) — PRESENT

When a user enables dark mode via the settings panel and then closes and reopens the
browser, the application reverts to light mode. The preference is not persisted.

### Steps to Reproduce (`### **Steps to Reproduce**`) — PRESENT

1. Open the application in a browser.
2. Navigate to Settings > Appearance.
3. Toggle "Dark Mode" to ON.
4. Close the browser completely.
5. Reopen the browser and navigate back to the application.

### Expected Result (`### **Expected Result**`) — PRESENT

The application should load in dark mode, matching the user's last preference.

### Actual Result (`### **Actual Result**`) — PRESENT

The application loads in light mode. The dark mode toggle is reset to OFF.

### Environment / Version (`### **Environment / Version**`) — PRESENT (but no version identifier)

> Not sure which version — using whatever is deployed on staging.

Observations:
- The section heading exists, so the required-section check passes.
- The content is vague: no explicit version number (e.g., `1.2.3`), no product-prefixed
  version (e.g., `ACME 2.1.0`), and no "version <number>" pattern.
- "whatever is deployed on staging" refers to an environment, not a version.
- Flagged for Step 4.5: version cannot be extracted -> gap flagging (4.5.6).

### Attachments (`### **Attachments**`) — PRESENT

None.

## Parsed Optional Sections

- **Root Cause** — not present
- **Suggested Fix** — not present

## Required-Section Check Result

All required sections are present. No missing sections — triage proceeds to Step 2.
