# Step 1 -- Bug Description Parsing

## Issue Metadata

- **Issue Key**: ACME-511
- **Web URL**: https://mock-jira.example.com/browse/ACME-511
- **Summary**: Dark mode toggle does not persist across browser sessions
- **Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID in Bug Configuration
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is NOT populated

## Template Validation

Bug template path: `docs/templates/bug-template.md`

All required sections are present in the bug description.

## Required Sections

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

**Analysis**: This section contains only vague text. No explicit version number
(e.g., `0.9.0`, `RHTPA 2.1.0`, `version 1.2.3`) can be extracted. The reporter
does not know which version they are using. This will be flagged in Step 4.5.

### Attachments

None.

## Optional Sections

- **Root Cause**: Not present in bug description.
- **Suggested Fix**: Not present in bug description.
