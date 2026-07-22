# Validation Result -- Bug Description Parsing (Step 1)

## Issue

**Key**: ACME-501
**Summary**: API returns 500 on malformed input
**Issue Type**: Bug (ID: 10020)

## Step 0 -- Configuration Validation

Configuration validated successfully from the project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 -- Fetch Bug

### Issue Type Validation

The issue type ID (`10020`) matches the Bug issue type ID from Bug Configuration. Issue confirmed as a Bug.

### Bug Description Parsing

The bug template defines the following **Required Sections** with their expected heading formats:

| Section              | Heading Format                  | Found in Description |
|----------------------|---------------------------------|----------------------|
| Description          | `### **Issue Description**`     | Yes                  |
| Steps to Reproduce   | `### **Steps to Reproduce**`    | No                   |
| Expected Result      | `### **Expected Result**`       | No                   |
| Actual Result        | `### **Actual Result**`         | Yes                  |
| Environment / Version| `### **Environment / Version**` | No                   |
| Attachments          | `### **Attachments**`           | Yes                  |

### Sections Present (3 of 6 required)

1. **Issue Description**: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. **Actual Result**: "HTTP 500 Internal Server Error with a stack trace in the response body."
3. **Attachments**: "None."

### Sections Missing (3 of 6 required)

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) -- not present in the bug description.
2. **Expected Result** (`### **Expected Result**`) -- not present in the bug description.
3. **Environment / Version** (`### **Environment / Version**`) -- not present in the bug description.

## Outcome

**Execution halted at Step 1.** The bug description does not conform to the required template.

Per the triage-bug skill protocol, when required sections are missing, the skill must stop immediately and report the gap to the user without attempting further investigation.

> Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md.

No further steps (Steps 2-7) were executed. The bug report must be updated to include the missing sections before triage can proceed.
