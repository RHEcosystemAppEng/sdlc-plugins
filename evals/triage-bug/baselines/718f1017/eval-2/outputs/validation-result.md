# Triage Bug: ACME-501

## Step 0 -- Config Validation

Extracted configuration from CLAUDE.md:

| Field | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Feature issue type ID | 10142 |
| Git Pull Request custom field | customfield_10875 |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

Configuration is complete. All required Bug Configuration fields are present (bug issue type ID, bug template path, bug-to-task link type).

## Step 1 -- Fetch Bug and Parse Description

### Issue Metadata

| Field | Value |
|---|---|
| Key | ACME-501 |
| Summary | API returns 500 on malformed input |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | production-incident |
| Component | api-gateway |

### Issue Type Validation

The issue type ID is **10020**, which matches the Bug Configuration's `Bug issue type ID: 10020`. Confirmed: this is a Bug issue.

### Required Sections (from bug template)

The bug template at `docs/templates/bug-template.md` defines the following required sections and their heading formats:

| Section | Heading Format |
|---|---|
| Issue Description | `### **Issue Description**` |
| Steps to Reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Attachments | `### **Attachments**` |

### Description Parsing Result

Parsing the bug description against the required template sections:

| Required Section | Status |
|---|---|
| Issue Description | FOUND |
| Steps to Reproduce | MISSING |
| Expected Result | MISSING |
| Actual Result | FOUND |
| Attachments | FOUND |

### Validation Error

Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

Execution stops here. The bug report is incomplete and cannot be triaged.

## Execution Stopped

Execution stopped at **Step 1 -- Fetch Bug and Parse Description** due to missing required sections in the bug description.

The following steps were **NOT executed**:

- Step 2 -- Locate Relevant Code (not executed)
- Step 3 -- Reproduce and Investigate (not executed)
- Step 4 -- Root Cause Analysis (not executed)
- Step 5 -- Create Implementation Tasks (not executed)
- Step 6 -- Link Tasks to Bug (not executed)
- Step 7 -- Update Bug with Findings (not executed)

No investigation was performed. No root cause analysis was attempted. No tasks were created. Do not attempt to investigate an incomplete bug report.

## Recommended Action

The reporter should update bug ACME-501 to include the missing required sections:

1. **Steps to Reproduce** -- Provide the exact steps to trigger the HTTP 500 error, including the malformed JSON payload used and the API endpoint called.
2. **Expected Result** -- Describe what the API should return instead (e.g., HTTP 400 Bad Request with a descriptive error message).

The bug description must follow the template at `docs/templates/bug-template.md`. Once the missing sections are added, the bug can be re-triaged.
