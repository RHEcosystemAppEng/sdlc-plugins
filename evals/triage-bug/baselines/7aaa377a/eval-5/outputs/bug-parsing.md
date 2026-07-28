# Bug Parsing — ACME-511 (Step 1)

## Metadata

| Field | Value |
|-------|-------|
| **Issue Key** | ACME-511 |
| **Summary** | Dark mode toggle does not persist across browser sessions |
| **Issue Type** | Bug (ID: 10020) |
| **Status** | New |
| **Labels** | reported-by-user |
| **Component** | sdlc-workflow |
| **Affects Version/s** | (none — `affectsVersions` field is empty) |
| **Web URL** | https://mock-jira.example.com/browse/ACME-511 |

## Issue Type Validation

- Configured Bug issue type ID (from CLAUDE.md): `10020`
- Actual issue type ID: `10020`
- Result: **Match — valid Bug issue** ✓

## Template Validation

Bug template read from: `docs/templates/bug-template.md`

Required sections per template:

| Section | Heading Format | Present in Issue |
|---------|----------------|-----------------|
| Description | `### **Issue Description**` | Yes ✓ |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes ✓ |
| Expected Result | `### **Expected Result**` | Yes ✓ |
| Actual Result | `### **Actual Result**` | Yes ✓ |
| Environment / Version | `### **Environment / Version**` | Yes ✓ |
| Attachments | `### **Attachments**` | Yes ✓ |

All required sections present — proceeding with triage.

## Parsed Required Sections

### Description

> When a user enables dark mode via the settings panel and then closes and reopens the
> browser, the application reverts to light mode. The preference is not persisted.

### Steps to Reproduce

1. Open the application in a browser.
2. Navigate to Settings > Appearance.
3. Toggle "Dark Mode" to ON.
4. Close the browser completely.
5. Reopen the browser and navigate back to the application.

### Expected Result

> The application should load in dark mode, matching the user's last preference.

### Actual Result

> The application loads in light mode. The dark mode toggle is reset to OFF.

### Environment / Version

> Not sure which version — using whatever is deployed on staging.

**Note**: This section contains vague, non-specific text. No version number or
recognizable version pattern (e.g., `0.9.0`, `ACME 2.1.0`) can be extracted.
This will be flagged during Step 4.5 (Affects Version Resolution).

### Attachments

> None.

## Parsed Optional Sections

| Section | Present | Content |
|---------|---------|---------|
| Root Cause | No | — |
| Suggested Fix | No | — |

Neither optional section was provided by the reporter.

## Affects Version Pre-check

- `affectsVersions` Jira field: **empty** (not pre-populated)
- Step 4.5 will attempt version resolution from the Environment / Version section content.
