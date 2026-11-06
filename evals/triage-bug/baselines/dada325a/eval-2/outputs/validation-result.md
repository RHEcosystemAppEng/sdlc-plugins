# Triage Bug Validation Result — ACME-501

## Outcome: STOPPED at Step 1 (Parse bug description)

Triage of **ACME-501** ("API returns 500 on malformed input") was halted during
Step 1 because the Bug description is missing required template sections. No
reproduction, codebase investigation, root cause analysis, Task creation, or Jira
linking was performed.

## Step 0 — Validate Project Configuration: PASSED

All required sections are present in the project CLAUDE.md (`claude-md-bug-config.md`):

| Section | Status | Extracted value |
|---|---|---|
| Repository Registry | Present (1 entry) | acme-backend (`serena_backend`) |
| Jira Configuration | Present | Project key: `ACME`, Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Present | No Serena instances configured |
| Bug Configuration | Present | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md`; Bug-to-Task link type: `Blocks` |

## Step 1 — Fetch Bug

### Issue type validation: PASSED

ACME-501 has `issuetype.id` = **10020**, which matches the configured Bug issue type
ID (10020). The issue is a Bug, so processing continued to description parsing.

### Bug description parsing: FAILED

The template (`bug-template-mock.md`) defines these heading formats. Each was matched
against the ACME-501 description:

**Required Sections**

| Section | Expected heading | Found in ACME-501? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | **No — MISSING** |
| Expected Result | `### **Expected Result**` | **No — MISSING** |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No — MISSING** |
| Attachments | `### **Attachments**` | Yes (content: "None.") |

**Optional Sections**

| Section | Expected heading | Found? |
|---|---|---|
| Root Cause | `### **Root Cause**` | No (optional, not an error) |
| Suggested Fix | `### **Suggested Fix**` | No (optional, not an error) |

Extracted content of the sections that were present:

- **Description:** The API gateway returns HTTP 500 when receiving a malformed JSON
  payload instead of returning a 400 Bad Request with a descriptive error message.
- **Actual Result:** HTTP 500 Internal Server Error with a stack trace in the response body.
- **Attachments:** None.

### Message to the user

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result,
> Environment / Version. The bug description does not follow the template at
> docs/templates/bug-template.md."

### Execution stopped

Per the skill, execution stops immediately when any Required Section is missing —
an incomplete bug report is not investigated. Therefore:

- Metadata extraction, Step 2 (Reproduce/Trace), Step 3 (Codebase Investigation),
  Step 4 (Root Cause comment), Step 4.5 (Affects Version), Step 5/5b/5c (Task creation,
  linking, digest), Step 6, and Step 7 were **not executed**.
- No Jira comments, Tasks, links, or field updates were made.
- The skill did not try to infer or fill in the missing sections (e.g., it did not
  guess reproduction steps from the summary, or assume an expected 400 response).

## Recommended next action

The reporter should update ACME-501 to add the missing sections:

1. `### **Steps to Reproduce**` — e.g., the endpoint, the request method, and a
   sample malformed JSON payload that triggers the 500.
2. `### **Expected Result**` — e.g., HTTP 400 Bad Request with a descriptive error message.
3. `### **Environment / Version**` — the deployed version/environment where the issue was seen.

Then re-run `/sdlc-workflow:triage-bug ACME-501`.
