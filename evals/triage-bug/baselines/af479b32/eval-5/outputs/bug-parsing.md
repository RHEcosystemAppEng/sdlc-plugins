# Step 1 -- Parsed Bug Description

## Bug Metadata

- **Issue Key**: ACME-511
- **Web URL**: https://mock-jira.example.com/browse/ACME-511
- **Summary**: Dark mode toggle does not persist across browser sessions
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is not populated

## Configuration Validation (Step 0)

Extracted from CLAUDE.md Bug Configuration:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Issue type validation: Bug issue type ID 10020 matches the configured Bug issue type ID 10020. Validated.

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

### Attachments

None.

## Optional Sections

### Root Cause

Not provided by reporter.

### Suggested Fix

Not provided by reporter.

## Parsing Outcome

All required sections are present. The bug description conforms to the template at `docs/templates/bug-template.md`. Proceeding with triage.

**Note on Environment / Version**: The section contains vague text ("Not sure which version -- using whatever is deployed on staging") with no extractable version identifier. This will be flagged during Step 4.5 (Affects Version Resolution).
