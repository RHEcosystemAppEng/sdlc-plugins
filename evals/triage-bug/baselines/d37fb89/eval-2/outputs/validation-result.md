# Triage Bug Validation Result -- ACME-501

## Step 0 -- Validate Project Configuration

Configuration validated successfully. Extracted values from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 -- Fetch Bug

### Issue type validation

Issue ACME-501 has issue type ID 10020, which matches the Bug issue type ID from Bug Configuration. Validation passed.

### Bug description parsing

The bug description template at `docs/templates/bug-template.md` defines the following **Required Sections**:

| Section | Heading Format | Present in ACME-501 |
|---------|----------------|---------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No -- MISSING** |
| Expected Result | `### **Expected Result**` | **No -- MISSING** |
| Actual Result | `### **Actual Result**` | Yes |

The template also defines **Optional Sections** (Attachments, Root Cause, Suggested Fix). The bug includes an Attachments section, but optional sections do not affect validation.

#### Sections found in ACME-501 description

1. `### **Issue Description**` -- "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. `### **Actual Result**` -- "HTTP 500 Internal Server Error with a stack trace in the response body."
3. `### **Attachments**` -- "None."

#### Sections missing from ACME-501 description

1. `### **Steps to Reproduce**` -- Not present anywhere in the bug description.
2. `### **Expected Result**` -- Not present anywhere in the bug description.

### Validation outcome -- FAILED

Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

**Execution stopped at Step 1.** Per the triage-bug skill specification, an incomplete bug report must not be investigated. Steps 2 through 7 (Reproduce/Trace, Codebase Investigation, Root Cause Analysis, Task Generation, Linking, and Reporting) were not executed.

### Recommended action

The bug reporter should update ACME-501 to include the missing sections before re-running `/triage-bug ACME-501`:

- **Steps to Reproduce**: Provide numbered steps to trigger the HTTP 500 error (e.g., the exact API endpoint, request method, headers, and malformed JSON payload used).
- **Expected Result**: Describe what should happen instead (e.g., "HTTP 400 Bad Request with a JSON error response describing the malformed input").
