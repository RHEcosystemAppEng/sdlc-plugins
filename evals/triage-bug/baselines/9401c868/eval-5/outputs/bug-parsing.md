# Step 1 -- Bug Parsing: ACME-511

## Configuration Validated (Step 0)

| Config Item              | Value                                  |
|--------------------------|----------------------------------------|
| Project key              | ACME                                   |
| Cloud ID                 | mock-cloud-id-for-eval                 |
| Bug issue type ID        | 10020                                  |
| Bug template path        | docs/templates/bug-template.md         |
| Bug-to-Task link type    | Blocks                                 |

## Issue Metadata

| Field              | Value                                                            |
|--------------------|------------------------------------------------------------------|
| Issue Key          | ACME-511                                                         |
| Summary            | Dark mode toggle does not persist across browser sessions        |
| Issue Type         | Bug (ID: 10020) -- matches Bug Configuration                    |
| Status             | New                                                              |
| Labels             | reported-by-user                                                 |
| Component          | sdlc-workflow                                                    |
| Affects Version/s  | (none) -- field is NOT populated                                 |
| Web URL            | https://mock-jira.example.com/browse/ACME-511                   |

## Parsed Description Sections

### Required Sections

All required sections are present per the bug template at `docs/templates/bug-template.md`.

#### Issue Description

> When a user enables dark mode via the settings panel and then closes and reopens the
> browser, the application reverts to light mode. The preference is not persisted.

#### Steps to Reproduce

> 1. Open the application in a browser.
> 2. Navigate to Settings > Appearance.
> 3. Toggle "Dark Mode" to ON.
> 4. Close the browser completely.
> 5. Reopen the browser and navigate back to the application.

#### Expected Result

> The application should load in dark mode, matching the user's last preference.

#### Actual Result

> The application loads in light mode. The dark mode toggle is reset to OFF.

#### Environment / Version

> Not sure which version -- using whatever is deployed on staging.

**Analysis**: The Environment / Version section is present but contains only vague text
with no extractable version identifier. No version number pattern (e.g., `0.9.0`,
`RHTPA 2.1.0`, `version 1.2.3`) was found. This will be flagged in Step 4.5.

#### Attachments

> None.

### Optional Sections

| Section        | Present? |
|----------------|----------|
| Root Cause     | No       |
| Suggested Fix  | No       |

## Validation Result

All required sections are present. Proceeding to Step 2.
