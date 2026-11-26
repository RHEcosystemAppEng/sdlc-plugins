# Triage-Bug Validation Result: ACME-501

**Outcome: STOPPED at Step 1 (Parse bug description). Missing required sections.**

## Step 0: Validate Project Configuration (PASSED)

All the required sections are in the project CLAUDE.md (`claude-md-bug-config.md`):

| Section | Status | Values |
|---|---|---|
| Repository Registry | Present | acme-backend (serena_backend, /home/dev/repos/acme-backend) |
| Jira Configuration | Present | Project key: ACME, Cloud ID: mock-cloud-id-for-eval |
| Code Intelligence | Present | Tool naming convention section exists |
| Bug Configuration | Present | Bug issue type ID: 10020; Bug template path: docs/templates/bug-template.md; Bug-to-Task link type: Blocks |

## Step 0.5: Jira Access (simulated)

No real Jira MCP or REST call was made. The issue data came from `bug-issue-missing-sections.md`.

## Step 1: Fetch Bug

### Issue type validation (PASSED)

- Issue `issuetype.id` = **10020** (Bug)
- Configured Bug issue type ID = **10020**
- These match, so the skill continued to description parsing.

### Bug description parsing (FAILED)

The skill read the template (`bug-template-mock.md`, which stands in for `docs/templates/bug-template.md`) and pulled the heading formats from its Required Sections and Optional Sections tables. Then it matched each heading against the ACME-501 description.

**Required sections (the five the skill checks):**

| Skill section | Template heading | Found in ACME-501? |
|---|---|---|
| Description | `### **Issue Description**` | Yes. "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request..." |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No, MISSING** |
| Expected Result | `### **Expected Result**` | **No, MISSING** |
| Actual Result | `### **Actual Result**` | Yes. "HTTP 500 Internal Server Error with a stack trace in the response body." |
| Environment / Version | `### **Environment / Version**` | **No, MISSING** |

The template also lists `### **Attachments**` as a required row. ACME-501 has that heading (content: "None."), so it does not add to the missing list.

**Optional sections:**

| Section | Template heading | Found? |
|---|---|---|
| Root Cause | `### **Root Cause**` | No (optional, so the gate is not affected) |
| Suggested Fix | `### **Suggested Fix**` | No (optional, so the gate is not affected) |

### Result

Three required sections are missing. The skill's rule says: "If any Required Section is missing from the Bug description, list the missing sections and inform the user... Stop execution immediately." So the skill showed this message:

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

**Execution stopped immediately.** The skill does not investigate an incomplete bug report.

## Steps not executed

These steps were skipped because Step 1 stopped the run:

- Step 1 metadata extraction (only partly recorded for this report: Summary "API returns 500 on malformed input", Labels `production-incident`, Component `api-gateway`, no Affects Version/s set)
- Step 2: Reproduce/Trace. It needs Steps to Reproduce, and that section is missing.
- Step 3: Codebase Investigation
- Step 4: Root Cause Analysis (no comment posted)
- Step 4.5: Affects Version Resolution. It needs Environment / Version, and that section is missing.
- Step 5 / 5b / 5c: No Task created, no link made, no digest posted
- Step 6: Decomposition Guard
- Step 7: Report Result. No Task was created, so there is no `/implement-task` suggestion.

## Recommended next action for the reporter

Edit ACME-501 and add these headings with content:

- `### **Steps to Reproduce**`: the exact request (endpoint, method, malformed JSON payload) that triggers the 500
- `### **Expected Result**`: for example, HTTP 400 Bad Request with a descriptive error message (this is implied in the Issue Description, but it must be stated in its own section)
- `### **Environment / Version**`: the api-gateway version or build and the deployment environment

Then re-run `/triage-bug ACME-501`.
