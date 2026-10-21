# Step 1 -- Bug Parsing: ACME-511

## Configuration Validated (Step 0)

| Parameter | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

## Issue Metadata

| Field | Value |
|---|---|
| Issue Key | ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none) |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |

Issue type validation: Bug issue type ID 10020 matches Bug Configuration. Proceeding.

Affects Version/s field is **not populated** -- Step 4.5 will attempt resolution from description content.

## Parsed Description Sections

### Template Headings (from bug-template.md)

| Section | Heading Format | Required |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | Yes |
| Attachments | `### **Attachments**` | Yes |
| Root Cause | `### **Root Cause**` | No (Optional) |
| Suggested Fix | `### **Suggested Fix**` | No (Optional) |

### Extracted Required Sections

**Issue Description:**

> When a user enables dark mode via the settings panel and then closes and reopens the browser, the application reverts to light mode. The preference is not persisted.

**Steps to Reproduce:**

> 1. Open the application in a browser.
> 2. Navigate to Settings > Appearance.
> 3. Toggle "Dark Mode" to ON.
> 4. Close the browser completely.
> 5. Reopen the browser and navigate back to the application.

**Expected Result:**

> The application should load in dark mode, matching the user's last preference.

**Actual Result:**

> The application loads in light mode. The dark mode toggle is reset to OFF.

**Environment / Version:**

> Not sure which version -- using whatever is deployed on staging.

**Attachments:**

> None.

### Extracted Optional Sections

- **Root Cause**: Not present in description.
- **Suggested Fix**: Not present in description.

### Validation Result

All 6 required sections are present. No missing sections. Proceeding to Step 2.
