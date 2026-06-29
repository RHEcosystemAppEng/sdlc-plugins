# Validation Result -- Step 1: Bug Description Parsing

## Issue

**Key**: ACME-501
**Summary**: API returns 500 on malformed input

## Bug Template Reference

**Bug template path**: docs/templates/bug-template.md (from Bug Configuration in CLAUDE.md)

## Required Sections Analysis

The bug description template defines the following Required Sections:

| Section | Heading Format | Status |
|---------|----------------|--------|
| Description | `### **Issue Description**` | FOUND |
| Steps to Reproduce | `### **Steps to Reproduce**` | MISSING |
| Expected Result | `### **Expected Result**` | MISSING |
| Actual Result | `### **Actual Result**` | FOUND |
| Attachments | `### **Attachments**` | FOUND |

### Sections Found (3 of 5)

1. **Issue Description** -- Present. Content: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. **Actual Result** -- Present. Content: "HTTP 500 Internal Server Error with a stack trace in the response body."
3. **Attachments** -- Present. Content: "None."

### Sections Missing (2 of 5)

1. **Steps to Reproduce** -- The `### **Steps to Reproduce**` heading is entirely absent from the bug description. There is no content between any headings that could serve as reproduction steps.
2. **Expected Result** -- The `### **Expected Result**` heading is entirely absent from the bug description. While the Issue Description implies the expected behavior (400 Bad Request), the structured section required by the template is not present.

## Optional Sections Analysis

| Section | Heading Format | Status |
|---------|----------------|--------|
| Root Cause | `### **Root Cause**` | NOT PRESENT |
| Suggested Fix | `### **Suggested Fix**` | NOT PRESENT |

No optional sections are present. This is acceptable -- optional sections do not trigger validation errors.

## Stop Decision

**Result: VALIDATION FAILURE -- Execution stopped at Step 1.**

Per the triage-bug skill specification (Step 1, "Parse bug description"):

> "If any Required Section is missing from the Bug description, list the missing sections and inform the user [...] Stop execution immediately. Do not attempt to investigate an incomplete bug report."

The skill halts with the following validation error:

> Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

Steps 2 through 5 (Reproduce/Trace, Codebase Investigation, Root Cause Analysis, Task creation, linking, and digest) are **not executed**. The incomplete bug report must be updated by the reporter to include the missing sections before triage can proceed.
