# Triage Bug ACME-501: Validation Result

**Outcome: STOPPED in Step 1 (Parse bug description). Required sections are missing.**

No investigation was done. No root cause comment was posted, no Task was created, and no links or digests were written. The skill says: "Do not attempt to investigate an incomplete bug report."

---

## Step 0: Validate Project Configuration (PASSED)

Source: `claude-md-bug-config.md`

| Requirement | Status | Value |
|---|---|---|
| Repository Registry (>= 1 entry) | Present | acme-backend (`serena_backend`, /home/dev/repos/acme-backend) |
| Jira Configuration: Project key | Present | ACME |
| Jira Configuration: Cloud ID | Present | mock-cloud-id-for-eval |
| Code Intelligence section | Present | "No Serena MCP servers are configured" |
| Bug Configuration: Bug issue type ID | Present | 10020 |
| Bug Configuration: Bug template path | Present | docs/templates/bug-template.md (mocked by `bug-template-mock.md`) |
| Bug Configuration: Bug-to-Task link type | Present | Blocks |

Minor observation: the Code Intelligence section exists but does not state the `mcp__<instance>__<tool>` naming convention. It also says no Serena servers are configured, but the Registry lists `serena_backend`. This did not block validation, and it does not matter here because execution stops in Step 1.

## Step 0.5: Jira Access

Simulated. Per the eval instructions, no Jira MCP or REST calls were made. The issue data came from `bug-issue-missing-sections.md`.

## Step 1: Fetch Bug

### Issue type validation (PASSED)

- Issue `issuetype.id` = **10020** (Bug)
- Configured Bug issue type ID = **10020**
- They match, so the skill continues to description parsing.

### Bug description parsing (FAILED)

The template (`bug-template-mock.md`) defines these heading formats:

**Required sections** checked against the ACME-501 description:

| Skill section | Template heading | Found in ACME-501? |
|---|---|---|
| Description | `### **Issue Description**` | Yes. "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message." |
| Steps to Reproduce | `### **Steps to Reproduce**` | **MISSING** |
| Expected Result | `### **Expected Result**` | **MISSING** |
| Actual Result | `### **Actual Result**` | Yes. "HTTP 500 Internal Server Error with a stack trace in the response body." |
| Environment / Version | `### **Environment / Version**` | **MISSING** |
| Attachments (listed as required in the template only) | `### **Attachments**` | Yes. "None." |

**Optional sections:**

| Section | Template heading | Found? |
|---|---|---|
| Root Cause | `### **Root Cause**` | Not present (optional, no action needed) |
| Suggested Fix | `### **Suggested Fix**` | Not present (optional, no action needed) |

**Missing required sections: Steps to Reproduce, Expected Result, Environment / Version.**

### Message presented to the user

> Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md.

**Execution stopped here.**

### Why stopping is correct

- Without **Steps to Reproduce**, Step 2 cannot reproduce or trace the bug, and Step 5 cannot write reproducer-test guidance.
- Without **Expected Result**, the reproducer test has nothing to assert after the fix, and the Bug Context section cannot be filled in.
- Without **Environment / Version**, Step 4.5 cannot work out the Affects Version.
- The skill's Important Rules say: "If the Bug description is incomplete (missing required sections), stop and inform the user — do not attempt to investigate without structured input."

### Metadata extracted before stopping (for reference only)

- Key: ACME-501
- Web URL: https://mock-jira.example.com/browse/ACME-501
- Summary: API returns 500 on malformed input
- Labels: production-incident
- Component: api-gateway
- Affects Version/s: not set

## Steps not executed

Steps 2, 3, 4, 4.5, 5, 5b, 5c, 6 and 7 did not run. No Jira writes happened: no comments, no Task, no issue link, no digest.

## Suggested remediation for the reporter

Edit ACME-501 and add these sections using the template headings, then re-run `/triage-bug ACME-501`:

- `### **Steps to Reproduce**`: the exact request, such as the endpoint, method, and a sample malformed JSON body
- `### **Expected Result**`: for example, HTTP 400 Bad Request with a descriptive error message
- `### **Environment / Version**`: the api-gateway / product version and the deployment environment
