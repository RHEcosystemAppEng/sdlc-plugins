# Step 1 -- Bug Description Parsing

**Bug**: ACME-511
**Summary**: Dark mode toggle does not persist across browser sessions
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Affects Version/s**: (none)
**Web URL**: https://mock-jira.example.com/browse/ACME-511

## Parsed Sections

Template used: `docs/templates/bug-template.md`

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

## Parsing Notes

All required sections from the bug template were present in the description:
- Issue Description: present
- Steps to Reproduce: present
- Expected Result: present
- Actual Result: present
- Environment / Version: present (but contains vague text, no version identifier)
- Attachments: present (none provided)

Optional sections not present:
- Root Cause: not provided
- Suggested Fix: not provided
