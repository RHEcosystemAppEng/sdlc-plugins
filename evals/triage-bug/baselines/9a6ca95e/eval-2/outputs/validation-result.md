# Validation Result -- Step 1: Bug Description Parsing

## Issue

**Key**: ACME-501
**Summary**: API returns 500 on malformed input

## Step 0 -- Validate Project Configuration

Configuration validated successfully from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 -- Fetch Bug

### Issue type validation

The issue type ID (10020) matches the Bug issue type ID from Bug Configuration (10020). Validation passed.

### Bug description parsing

The bug description template defines the following **Required Sections**:

| Section | Heading Format | Present in ACME-501 |
|---------|----------------|---------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No** |
| Expected Result | `### **Expected Result**` | **No** |
| Actual Result | `### **Actual Result**` | Yes |
| Attachments | `### **Attachments**` | Yes |

**Parsing details:**

The description of ACME-501 was scanned for each required heading format defined in the bug template. Three sections were found and their content was extractable:

- **Issue Description**: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
- **Actual Result**: "HTTP 500 Internal Server Error with a stack trace in the response body."
- **Attachments**: "None."

Two required sections were **not found** in the description:

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) -- This heading does not appear anywhere in the bug description. Without steps to reproduce, investigation cannot proceed because there is no structured way to trace or reproduce the reported behavior.
2. **Expected Result** (`### **Expected Result**`) -- This heading does not appear anywhere in the bug description. Without an expected result, there is no defined target behavior to compare against the actual result.

### Validation outcome

**FAILED** -- Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

> Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result. The bug description does not follow the template at docs/templates/bug-template.md.

**Execution stopped at Step 1.** Steps 2 through 5 (Reproduce/Trace, Codebase Investigation, Root Cause Analysis, Generate Task) were not attempted because the skill requires a complete bug description before proceeding with investigation.
