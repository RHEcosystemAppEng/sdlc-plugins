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

The bug description template at `docs/templates/bug-template.md` defines the following **Required Sections**:

| Section | Heading Format | Present in ACME-501 |
|---------|----------------|---------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No** |
| Expected Result | `### **Expected Result**` | **No** |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No** |
| Attachments | `### **Attachments**` | Yes |

**Sections found in ACME-501 description:**

1. `### **Issue Description**` -- "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. `### **Actual Result**` -- "HTTP 500 Internal Server Error with a stack trace in the response body."
3. `### **Attachments**` -- "None."

**Sections missing from ACME-501 description:**

1. `### **Steps to Reproduce**`
2. `### **Expected Result**`
3. `### **Environment / Version**`

### Validation outcome: FAILED

Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**, **Environment / Version**. The bug description does not follow the template at `docs/templates/bug-template.md`.

**Execution stopped.** Per the triage-bug skill specification (Step 1), when any Required Section is missing from the Bug description, the skill must stop immediately and not attempt to investigate an incomplete bug report. Steps 2 through 7 were not executed.

## What happened

During Step 1 (Fetch Bug), the skill parsed the ACME-501 bug description by matching the heading formats defined in the bug description template. The template specifies six required sections identified by their exact heading format (e.g., `### **Steps to Reproduce**`). The skill scanned the bug description for each required heading and found only three of the six present. Three required sections -- Steps to Reproduce, Expected Result, and Environment / Version -- were absent from the description entirely.

Because the bug description is incomplete, the skill cannot proceed to investigation. Steps to Reproduce is needed by Step 2 (Reproduce/Trace) to understand and reproduce the bug. Expected Result is needed to compare against Actual Result and determine correct behavior. Environment / Version is needed by Step 4.5 (Affects Version Resolution) to resolve the version field. Without these sections, investigation would be based on incomplete and unstructured information, which violates the skill's guardrail: "Do not attempt to investigate without structured input."

The user should update the ACME-501 bug description to include the missing sections following the template at `docs/templates/bug-template.md`, then re-run `/triage-bug ACME-501`.
