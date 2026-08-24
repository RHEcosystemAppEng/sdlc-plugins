# Bug Parsing -- Step 1

## Issue Metadata

- **Issue Key**: ACME-511
- **Web URL**: https://mock-jira.example.com/browse/ACME-511
- **Summary**: Dark mode toggle does not persist across browser sessions
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is not populated

## Issue Type Validation

Bug issue type ID from Bug Configuration: 10020
Issue's actual type ID: 10020
Result: **Match** -- issue is a valid Bug.

## Bug Template

Template path: `docs/templates/bug-template.md`

### Required Sections (from template)

| Section | Heading Format | Found | Content |
|---------|----------------|-------|---------|
| Description | `### **Issue Description**` | Yes | See below |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes | See below |
| Expected Result | `### **Expected Result**` | Yes | See below |
| Actual Result | `### **Actual Result**` | Yes | See below |
| Environment / Version | `### **Environment / Version**` | Yes | See below |
| Attachments | `### **Attachments**` | Yes | None |

### Optional Sections (from template)

| Section | Heading Format | Found |
|---------|----------------|-------|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

All required sections are present. Proceeding with triage.

## Parsed Section Content

### Issue Description

When a user enables dark mode via the settings panel and then closes and reopens the
browser, the application reverts to light mode. The preference is not persisted.

### Steps to Reproduce

1. Open the application in a browser.
2. Navigate to Settings > Appearance.
3. Toggle "Dark Mode" to ON.
4. Close the browser completely.
5. Reopen the browser and navigate back to the application.

### Expected Result

The application should load in dark mode, matching the user's last preference.

### Actual Result

The application loads in light mode. The dark mode toggle is reset to OFF.

### Environment / Version

Not sure which version -- using whatever is deployed on staging.

### Attachments

None.
