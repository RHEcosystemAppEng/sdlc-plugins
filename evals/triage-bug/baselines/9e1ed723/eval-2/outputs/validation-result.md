# Triage-Bug Validation Result — ACME-501

**Outcome: STOPPED at Step 1 (Parse bug description) — Bug is missing required sections.**

## Step 0 – Validate Project Configuration: PASSED

Source: `claude-md-bug-config.md`

| Required item | Status | Value |
|---|---|---|
| Repository Registry (>= 1 entry) | Present | acme-backend (serena_backend, /home/dev/repos/acme-backend) |
| Jira Configuration – Project key | Present | ACME |
| Jira Configuration – Cloud ID | Present | mock-cloud-id-for-eval |
| Code Intelligence section | Present | (states no Serena servers configured) |
| Bug Configuration – Bug issue type ID | Present | 10020 |
| Bug Configuration – Bug template path | Present | docs/templates/bug-template.md (mocked by `bug-template-mock.md`) |
| Bug Configuration – Bug-to-Task link type | Present | Blocks |

## Step 0.5 – Jira Access

Not exercised (eval mode: no Jira MCP / REST calls). Issue data was read from `bug-issue-missing-sections.md` in place of `jira.get_issue(ACME-501)`.

## Step 1 – Fetch Bug

### Issue type validation: PASSED

- Issue `issuetype.id` = **10020** (Bug)
- Configured Bug issue type ID = **10020**
- Match, so parsing continues.

### Parse bug description: FAILED

The heading formats came from the template's Required Sections and Optional Sections tables. I compared them with the headings in the ACME-501 description:

| Required Section (skill) | Template heading | Found in ACME-501? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No — MISSING** |
| Expected Result | `### **Expected Result**` | **No — MISSING** |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No — MISSING** |

The template also lists `### **Attachments**` as a required section. It is present ("None."), so it does not count as a gap. The skill's own list of required sections does not include it either.

| Optional Section | Template heading | Found? |
|---|---|---|
| Root Cause | `### **Root Cause**` | No (optional, fine) |
| Suggested Fix | `### **Suggested Fix**` | No (optional, fine) |

Content extracted from the sections that are present:
- **Description**: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
- **Actual Result**: "HTTP 500 Internal Server Error with a stack trace in the response body."

### Message to user (per SKILL.md Step 1)

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

### Execution halted

As the skill requires, **execution stopped immediately** after the message above. "Do not attempt to investigate an incomplete bug report." As a result:

- Metadata extraction (Step 1) was not continued beyond what is needed to report.
- No reproduction or code tracing (Step 2) was done.
- No codebase investigation (Step 3) was done. No Serena or Read/Grep calls were made against acme-backend.
- No root cause comment (Step 4) was posted.
- No Affects Version resolution (Step 4.5) was done.
- No Task was created (Step 5), no issue link was made (Step 5b), and no digest comment was posted (Step 5c).
- No Jira writes of any kind were performed.

## Recommended next action

The reporter should update ACME-501 with these three sections, using the template headings:

- `### **Steps to Reproduce**`: the exact request (endpoint, method, malformed payload) that triggers the 500
- `### **Expected Result**`: for example, HTTP 400 Bad Request with a descriptive error message
- `### **Environment / Version**`: the deployed api-gateway / acme-backend version and environment

After that, re-run `/triage-bug ACME-501`.
