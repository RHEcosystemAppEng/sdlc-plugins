# Step 1 -- Bug Description Validation Result

## Issue

**Key**: ACME-501
**Summary**: API returns 500 on malformed input

## Validation Outcome: FAILED

Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

### Required Sections Check

The bug description template at `docs/templates/bug-template.md` defines the following required sections:

| Required Section | Heading Format | Present in Bug? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No -- MISSING** |
| Expected Result | `### **Expected Result**` | **No -- MISSING** |
| Actual Result | `### **Actual Result**` | Yes |
| Attachments | `### **Attachments**` | Yes |

### Sections Found in Bug Description

The bug description for ACME-501 contains only three of the five required sections:

1. `### **Issue Description**` -- Present. Describes the API gateway returning HTTP 500 on malformed JSON payloads.
2. `### **Actual Result**` -- Present. States "HTTP 500 Internal Server Error with a stack trace in the response body."
3. `### **Attachments**` -- Present. States "None."

### Missing Sections

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) -- This required section is entirely absent from the bug description. Without steps to reproduce, the triage process cannot trace code paths or construct a reproducer test.
2. **Expected Result** (`### **Expected Result**`) -- This required section is entirely absent from the bug description. Without the expected result, it is impossible to determine the correct behavior the fix should restore.

## Execution Stopped

Per the triage-bug skill Step 1 rules: "If any Required Section is missing from the Bug description, list the missing sections and inform the user. Stop execution immediately. Do not attempt to investigate an incomplete bug report."

**Steps 2 through 5 were NOT executed.** The skill stopped at Step 1 validation because the bug description is incomplete.

The reporter should update Bug ACME-501 to include the missing sections following the template at `docs/templates/bug-template.md`, then re-run `/triage-bug ACME-501`.
