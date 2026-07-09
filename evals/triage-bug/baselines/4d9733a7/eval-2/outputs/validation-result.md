# Validation Result -- Step 1: Bug Description Parsing

## Issue

**Key**: ACME-501
**Summary**: API returns 500 on malformed input

## Step 0 -- Validate Project Configuration

Project Configuration was read from CLAUDE.md (claude-md-bug-config.md). All required sections are present:

- **Repository Registry**: Contains `acme-backend` entry
- **Jira Configuration**: Project key `ACME`, Cloud ID `mock-cloud-id-for-eval`
- **Code Intelligence**: Present (no Serena instances configured)
- **Bug Configuration**: Present with all required fields:
  - Bug issue type ID: `10020`
  - Bug template path: `docs/templates/bug-template.md`
  - Bug-to-Task link type: `Blocks`

Configuration validation passed. Proceeding to Step 1.

## Step 1 -- Fetch Bug

### Issue Type Validation

The issue type ID on ACME-501 is `10020` (Bug). This matches the Bug issue type ID (`10020`) from Bug Configuration. Issue type validation passed.

### Bug Description Parsing

The bug description template at `docs/templates/bug-template.md` defines the following **Required Sections** with specific heading formats:

| Section | Heading Format | Present in ACME-501? |
|---------|----------------|----------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **NO -- MISSING** |
| Expected Result | `### **Expected Result**` | **NO -- MISSING** |
| Actual Result | `### **Actual Result**` | Yes |

The bug description template also defines these **Optional Sections**:

| Section | Heading Format | Present in ACME-501? |
|---------|----------------|----------------------|
| Attachments | `### **Attachments**` | Yes |
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

### Sections Found in ACME-501

The description of ACME-501 contains only the following headings:

1. `### **Issue Description**` -- "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. `### **Actual Result**` -- "HTTP 500 Internal Server Error with a stack trace in the response body."
3. `### **Attachments**` -- "None."

### Missing Required Sections

Two required sections are absent from the bug description:

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) -- There is no heading matching this format anywhere in the ACME-501 description. Without Steps to Reproduce, triage cannot determine how to reproduce the bug, trace the code path, or generate a reproducer test for the fix task.

2. **Expected Result** (`### **Expected Result**`) -- There is no heading matching this format anywhere in the ACME-501 description. Without Expected Result, triage cannot determine what the correct behavior should be, which is essential for both root cause analysis and for defining the reproducer test's pass condition.

## Outcome -- VALIDATION ERROR (Execution Stopped)

Step 1 terminated with a validation error. The skill did NOT proceed to Steps 2 through 7.

Per the triage-bug skill specification (SKILL.md, Step 1 -- "Parse bug description"):

> "If any Required Section is missing from the Bug description, list the missing sections and inform the user ... Stop execution immediately. Do not attempt to investigate an incomplete bug report."

The error message returned to the user:

> Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

### Why Execution Stopped

The triage-bug skill requires all four required sections to be present before proceeding with investigation. Steps to Reproduce is needed in Step 2 (Reproduce/Trace) to understand and reproduce the bug behavior. Expected Result is needed in Step 2 to compare against Actual Result, and in Step 5 to generate the reproducer test's pass/fail assertions. Without these sections, the skill cannot produce a meaningful root cause analysis or a well-defined fix task.

### Required Action

The bug reporter must update ACME-501 to include the missing sections following the heading formats defined in the bug template at `docs/templates/bug-template.md`. Once the description is complete, the user can re-run `/triage-bug ACME-501`.
