# Triage Bug — Validation Result for ACME-501

## Step 0 — Configuration Validation

The project CLAUDE.md contains a **Bug Configuration** section with all required fields:

- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Configuration validation passed.

## Step 1 — Fetch Bug and Parse

### Issue Type Validation

ACME-501 has issue type **Bug (ID: 10020)**, which matches the Bug issue type ID (10020) in the Bug Configuration. Issue type validation **passed**.

### Required Heading Formats from Template

The bug template at `docs/templates/bug-template.md` defines the following required sections in its Required Sections table:

| Section            | Heading Format               |
|--------------------|------------------------------|
| Description        | `### **Issue Description**`  |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result    | `### **Expected Result**`    |
| Actual Result      | `### **Actual Result**`      |
| Attachments        | `### **Attachments**`        |

### Bug Description Parsing

The description of ACME-501 was parsed by matching against the required heading formats listed above. The following results were found:

**Sections present:**

- `### **Issue Description**` — found. Contains: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
- `### **Actual Result**` — found. Contains: "HTTP 500 Internal Server Error with a stack trace in the response body."
- `### **Attachments**` — found. Contains: "None."

**Required sections MISSING:**

- `### **Steps to Reproduce**` — not found in the bug description.
- `### **Expected Result**` — not found in the bug description.

### Stop Decision

**Execution halted.** Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

Because required sections are missing, the triage-bug skill stops at Step 1 and does **not** proceed to Steps 2-5 (investigation, root cause analysis, task creation). The bug reporter must update ACME-501 to include the missing sections before triage can continue.
