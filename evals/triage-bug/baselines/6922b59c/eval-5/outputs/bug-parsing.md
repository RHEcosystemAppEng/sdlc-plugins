# Step 1 -- Bug Parsing: ACME-511

## Metadata

- **Issue Key**: ACME-511
- **Web URL**: https://mock-jira.example.com/browse/ACME-511
- **Summary**: Dark mode toggle does not persist across browser sessions
- **Issue Type**: Bug (ID: 10020) -- matches Bug Configuration (10020) -- validated
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is NOT populated

## Required Sections (parsed from description)

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

## Optional Sections

- **Root Cause**: not present in bug description
- **Suggested Fix**: not present in bug description

## Validation Result

All required sections are present per the bug template at `docs/templates/bug-template.md`. Proceeding with triage.
