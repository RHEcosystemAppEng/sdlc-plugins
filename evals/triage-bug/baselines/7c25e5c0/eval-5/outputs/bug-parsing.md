# Step 1 -- Parse Bug Description

**Bug Key**: ACME-511
**Summary**: Dark mode toggle does not persist across browser sessions
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Affects Version/s**: (none)

---

## Parsed Sections

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

---

## Template Conformance

All required sections from the bug template are present:

| Section | Present | Content |
|---------|---------|---------|
| Issue Description | Yes | Describes the dark mode persistence failure |
| Steps to Reproduce | Yes | 5 clear steps provided |
| Expected Result | Yes | Dark mode should persist |
| Actual Result | Yes | Reverts to light mode on reopen |
| Environment / Version | Yes | Vague -- no specific version identifier provided |
| Attachments | Yes | None |
