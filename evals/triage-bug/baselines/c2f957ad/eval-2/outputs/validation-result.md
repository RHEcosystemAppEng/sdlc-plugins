# Triage-Bug Validation Result: ACME-501

**Outcome: STOPPED in Step 1 (Parse bug description). Required sections are missing.**

The skill stopped here. No reproduction, codebase investigation, root cause comment, Affects Version update, Task creation, link, or digest comment was done.

## Step 0 – Validate Project Configuration: PASSED

Source: `claude-md-bug-config.md`

| Required section | Status | Extracted value |
|---|---|---|
| Repository Registry | Present (1 entry) | acme-backend, Serena instance `serena_backend`, `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key `ACME`, Cloud ID `mock-cloud-id-for-eval` |
| Code Intelligence | Present | No Serena MCP servers configured |
| Bug Configuration | Present | Bug issue type ID `10020`, Bug template path `docs/templates/bug-template.md`, Bug-to-Task link type `Blocks` |

## Step 0.5 – Jira Access

This is an eval, so the Jira MCP was not called. The issue data came from `bug-issue-missing-sections.md`.

## Step 1 – Fetch Bug

### Validate issue type: PASSED

- Issue `ACME-501` has issue type `Bug (ID: 10020)`.
- This matches the configured Bug issue type ID `10020`.

### Parse bug description: FAILED

I read the template at the Bug template path (mocked by `bug-template-mock.md`) and took the heading formats from its Required and Optional Sections tables. I then matched those headings against the description of ACME-501.

**Required sections (the five defined by the skill):**

| Section | Expected heading | Found in ACME-501? | Content |
|---|---|---|---|
| Description | `### **Issue Description**` | Yes | "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message." |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No (MISSING)** | — |
| Expected Result | `### **Expected Result**` | **No (MISSING)** | — |
| Actual Result | `### **Actual Result**` | Yes | "HTTP 500 Internal Server Error with a stack trace in the response body." |
| Environment / Version | `### **Environment / Version**` | **No (MISSING)** | — |

The template also lists `### **Attachments**` as a required section. It is present in ACME-501 with the content "None." The skill does not include Attachments in its list of five required sections, so it has no effect on the result either way.

**Optional sections:**

| Section | Expected heading | Found? |
|---|---|---|
| Root Cause | `### **Root Cause**` | No (optional, so no impact) |
| Suggested Fix | `### **Suggested Fix**` | No (optional, so no impact) |

### Message to the user

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

**Execution stopped immediately**, as Step 1 and the skill's Important Rules require: "If the Bug description is incomplete (missing required sections), stop and inform the user — do not attempt to investigate without structured input."

## Steps not executed

- Metadata extraction (Step 1 remainder). Metadata visible in the issue: Summary "API returns 500 on malformed input", Labels `production-incident`, Component `api-gateway`, Web URL https://mock-jira.example.com/browse/ACME-501, Affects Version/s not set.
- Step 2 Reproduce/Trace: not possible without Steps to Reproduce.
- Step 3 Codebase Investigation, Step 4 Root Cause Analysis (no Jira comment posted)
- Step 4.5 Affects Version Resolution: the Environment / Version section is missing in any case.
- Step 5 / 5b / 5c: no Task created, no link, no digest.
- Step 6 Decomposition Guard, Step 7 Report Result

## Recommended next action

The reporter should update ACME-501 to add these sections:
- `### **Steps to Reproduce**`: for example, the endpoint, the HTTP method, and the exact malformed JSON payload sent.
- `### **Expected Result**`: for example, HTTP 400 Bad Request with a descriptive error message.
- `### **Environment / Version**`: the deployed api-gateway / acme-backend version and the environment.

Then re-run `/triage-bug ACME-501`.
