# Triage Bug ACME-501 — Validation Result

**Outcome: STOPPED at Step 1 (Parse bug description) — missing required sections.**

No investigation, root cause analysis, Jira comment, Affects Version update, Task
creation, link, or digest was performed.

## Step 0 – Validate Project Configuration: PASSED

From `claude-md-bug-config.md`:

| Item | Value |
|---|---|
| Repository Registry | 1 entry (acme-backend, serena_backend) |
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Code Intelligence | section present |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md (simulated by `bug-template-mock.md`) |
| Bug-to-Task link type | Blocks |

## Step 0.5 – Jira Access

Simulated; issue data read from `bug-issue-missing-sections.md` (no MCP/REST calls made).

## Step 1 – Fetch Bug

### Issue type validation: PASSED

ACME-501 has Issue Type "Bug" with ID **10020**, matching the configured Bug issue
type ID **10020**.

### Bug description parsing: FAILED

Heading formats were taken from the template's Required Sections table and matched
against the ACME-501 description.

| Required section | Expected heading | Found in ACME-501? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No — MISSING** |
| Expected Result | `### **Expected Result**` | **No — MISSING** |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No — MISSING** |
| Attachments* | `### **Attachments**` | Yes ("None.") |

\* Attachments is listed in the template's Required Sections table but is not one of
the five required sections the skill uses for its gate. It is present anyway, so it
does not change the outcome.

Optional sections (`### **Root Cause**`, `### **Suggested Fix**`): neither present
(this is allowed).

Extracted content of the sections that were found:
- **Description**: The API gateway returns HTTP 500 on a malformed JSON payload
  instead of a 400 Bad Request with a descriptive error message.
- **Actual Result**: HTTP 500 Internal Server Error with a stack trace in the response body.

### Message to the user

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result,
> Environment / Version. The bug description does not follow the template at
> docs/templates/bug-template.md."

**Execution stopped immediately**, as the skill requires: "Do not attempt to
investigate an incomplete bug report." So Steps 2–7 did not run. Metadata
extraction (summary, labels `production-incident`, component `api-gateway`)
did not matter because the skill stopped first.

## Why this matters

- Without **Steps to Reproduce**, Step 2 cannot reproduce or trace the bug, and the
  reproducer test (first acceptance criterion) cannot be specified.
- Without **Expected Result**, the reproducer test has nothing to assert after the fix.
  (The Description suggests 400 Bad Request, but the skill does not infer missing
  sections.)
- Without **Environment / Version**, Step 4.5 cannot work out the Affects Version.

## Recommended next action

The reporter should update ACME-501 to add the three missing sections using the
template headings, then re-run `/triage-bug ACME-501`.
