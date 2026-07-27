# Step 1 -- Fetch Bug: Parsed Description Sections

## Configuration Validated (Step 0)

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Issue Metadata

- **Issue Key**: ACME-511
- **Web URL**: https://mock-jira.example.com/browse/ACME-511
- **Summary**: Dark mode toggle does not persist across browser sessions
- **Issue Type**: Bug (ID: 10020) -- matches Bug Configuration (valid)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is NOT populated

## Required Sections (parsed from description using template headings)

### Issue Description
> When a user enables dark mode via the settings panel and then closes and reopens the
> browser, the application reverts to light mode. The preference is not persisted.

### Steps to Reproduce
> 1. Open the application in a browser.
> 2. Navigate to Settings > Appearance.
> 3. Toggle "Dark Mode" to ON.
> 4. Close the browser completely.
> 5. Reopen the browser and navigate back to the application.

### Expected Result
> The application should load in dark mode, matching the user's last preference.

### Actual Result
> The application loads in light mode. The dark mode toggle is reset to OFF.

### Environment / Version
> Not sure which version -- using whatever is deployed on staging.

**Analysis**: The Environment / Version section is present but contains only vague text
with no extractable version identifier. No explicit version number, product-prefixed
version, or version keyword followed by a number is present. This will trigger
Step 4.5.6 (gap flagging) during Affects Version Resolution.

### Attachments
> None.

## Optional Sections

- **Root Cause**: Not present in the bug description.
- **Suggested Fix**: Not present in the bug description.

## Validation Result

All 5 required sections are present in the bug description. The description conforms
to the bug template at `docs/templates/bug-template.md`. Proceeding to Step 2.
