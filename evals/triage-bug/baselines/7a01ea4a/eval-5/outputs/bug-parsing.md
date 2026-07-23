# Step 1 -- Bug Parsing: ACME-511

## Metadata

- **Issue Key**: ACME-511
- **Web URL**: https://mock-jira.example.com/browse/ACME-511
- **Summary**: Dark mode toggle does not persist across browser sessions
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is not populated

## Configuration Validation (Step 0)

Validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Issue type matches Bug Configuration (10020 = 10020). Proceeding.

## Parsed Required Sections

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

## Parsed Optional Sections

- **Root Cause**: not present
- **Suggested Fix**: not present

## Validation Result

All required sections are present. No missing sections detected.
