# Triage-Bug Validation Result — ACME-501

## Outcome

**Execution stopped in Step 1 (Fetch Bug -> Parse bug description).** The Bug description
is missing required template sections. No investigation, root cause comment, Affects
Version update, Task creation, link, or digest was performed.

Message to the user:

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result,
> Environment / Version. The bug description does not follow the template at
> docs/templates/bug-template.md."

## Step 0 — Validate Project Configuration: PASSED

From `claude-md-bug-config.md` (`# Project Configuration`):

| Check | Result |
|---|---|
| Repository Registry (>= 1 entry) | Present — `acme-backend` (serena_backend, /home/dev/repos/acme-backend) |
| Jira Configuration (Project key, Cloud ID) | Present — `ACME`, `mock-cloud-id-for-eval` |
| Code Intelligence | Present (states no Serena servers configured) |
| Bug Configuration — Bug issue type ID | `10020` |
| Bug Configuration — Bug template path | `docs/templates/bug-template.md` (mock content: `bug-template-mock.md`) |
| Bug Configuration — Bug-to-Task link type | `Blocks` |

## Step 0.5 — Jira Access: not exercised

Per eval instructions, no Jira MCP/REST calls were made; the issue was read from
`bug-issue-missing-sections.md`.

## Step 1 — Fetch Bug

### Issue type validation: PASSED

Issue type ID of ACME-501 is `10020`, matching the configured Bug issue type ID `10020`.

### Parse bug description: FAILED

Heading formats extracted from the bug template (Required / Optional Sections tables),
matched against the ACME-501 description:

| Section (skill mapping) | Template heading | Found in ACME-501? |
|---|---|---|
| Description | `### **Issue Description**` | Yes — "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message." |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No — MISSING** |
| Expected Result | `### **Expected Result**` | **No — MISSING** |
| Actual Result | `### **Actual Result**` | Yes — "HTTP 500 Internal Server Error with a stack trace in the response body." |
| Environment / Version | `### **Environment / Version**` | **No — MISSING** |
| Attachments (template-only required row) | `### **Attachments**` | Yes — "None." |
| Root Cause (optional) | `### **Root Cause**` | Not present (optional, OK) |
| Suggested Fix (optional) | `### **Suggested Fix**` | Not present (optional, OK) |

Note: the 400 Bad Request wording appears inside the Issue Description prose, but there
is no `### **Expected Result**` heading, so the Expected Result section is treated as
missing. Sections are found by matching headings, not by guessing from the prose.

**Missing required sections:** Steps to Reproduce, Expected Result, Environment / Version.

### Action taken

Following SKILL.md Step 1 ("If any Required Section is missing ... Stop execution
immediately. Do not attempt to investigate an incomplete bug report") and the Important
Rule ("If the Bug description is incomplete ... stop and inform the user"):

- Execution halted after Step 1 parsing.
- Metadata extraction, Steps 2–7 were **not** executed.
- No Jira comments, Task, issue link, Affects Version edit, or digest were produced.

## Recommended next step for the reporter

Update ACME-501's description to include the missing sections using the template
headings:

- `### **Steps to Reproduce**` — e.g., the exact request (endpoint, method, malformed JSON body) sent to the API gateway
- `### **Expected Result**` — e.g., HTTP 400 Bad Request with a descriptive error message
- `### **Environment / Version**` — the api-gateway / product version and environment where the 500 was seen

Then re-run `/triage-bug ACME-501`.
