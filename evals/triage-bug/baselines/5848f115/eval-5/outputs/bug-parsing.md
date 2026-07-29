# Step 1 -- Bug Parsing: ACME-511

## Configuration Validated (Step 0)

| Config Field | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

## Issue Metadata

| Field | Value |
|---|---|
| Issue key | ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Issue Type | Bug (ID: 10020) -- matches Bug Configuration |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none) -- field is empty, no versions populated |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |

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

**Analysis**: This section contains only vague text. No explicit version number
(e.g., `0.9.0`, `RHTPA 2.1.0`) or version pattern can be extracted. The reporter
does not know which version they are using. This will trigger the Affects Version
gap flow in Step 4.5.

### Attachments

None.

## Parsed Optional Sections

| Section | Present? |
|---|---|
| Root Cause | No |
| Suggested Fix | No |

## Validation Result

All five required sections are present in the bug description. The description
conforms to the template at `docs/templates/bug-template.md`. Proceeding with
investigation.
