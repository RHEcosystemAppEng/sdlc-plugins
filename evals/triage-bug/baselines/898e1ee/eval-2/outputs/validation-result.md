# Triage Bug Validation Result: ACME-501

## Execution Summary

**Skill**: triage-bug
**Issue**: ACME-501 — API returns 500 on malformed input
**Outcome**: STOPPED at Step 1 — Bug description is missing required sections.

---

## Step 0 — Validate Project Configuration

Configuration validated successfully. Extracted values:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 — Fetch Bug

### Issue type validation

The issue type ID on ACME-501 is `10020`, which matches the Bug issue type ID from Bug Configuration (`10020`). Issue type validation passed.

### Bug description parsing

Read the bug description template at the configured **Bug template path** (`docs/templates/bug-template.md`). The template defines the following required sections and their heading formats:

| Required Section | Heading Format | Present in ACME-501? |
|---|---|---|
| Description | `### **Issue Description**` | YES |
| Steps to Reproduce | `### **Steps to Reproduce**` | NO |
| Expected Result | `### **Expected Result**` | NO |
| Actual Result | `### **Actual Result**` | YES |
| Attachments | `### **Attachments**` | YES |

**Parsing details:**

The bug description for ACME-501 contains only three of the five required section headings:

1. `### **Issue Description**` — found with content: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. `### **Actual Result**` — found with content: "HTTP 500 Internal Server Error with a stack trace in the response body."
3. `### **Attachments**` — found with content: "None."

Two required sections are entirely absent from the description:

- **Steps to Reproduce** (`### **Steps to Reproduce**`) — no heading matching this format exists in the bug description.
- **Expected Result** (`### **Expected Result**`) — no heading matching this format exists in the bug description.

### Result: Execution STOPPED

Per the triage-bug skill specification (Step 1, "Parse bug description"):

> "If any Required Section is missing from the Bug description, list the missing sections and inform the user [...] Stop execution immediately. Do not attempt to investigate an incomplete bug report."

The following message would be reported to the user:

> "Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`."

## Steps 2-7 — NOT EXECUTED

Steps 2 through 7 were not executed. The skill halted at Step 1 because the bug description is incomplete. The missing "Steps to Reproduce" and "Expected Result" sections are required for the triage-bug workflow to proceed with reproduction, codebase investigation, root cause analysis, and task generation.

The reporter must update ACME-501 to include all required sections per the bug template before this skill can be re-run.
