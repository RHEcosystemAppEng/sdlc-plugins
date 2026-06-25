# triage-bug Validation Result: ACME-501

## Step 0 -- Config Validation

Extracted configuration from CLAUDE.md `# Project Configuration`:

| Field | Value |
|-------|-------|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

All required sections present (`## Repository Registry`, `## Jira Configuration`, `## Code Intelligence`, `## Bug Configuration`). Configuration is **valid**.

---

## Step 1 -- Fetch Bug

### Issue Metadata

| Field | Value |
|-------|-------|
| Key | ACME-501 |
| Summary | API returns 500 on malformed input |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | production-incident |
| Component | api-gateway |
| Web URL | https://mock-jira.example.com/browse/ACME-501 |

### Issue Type Validation

The issue's type ID **10020** matches the Bug issue type ID from Bug Configuration (**10020**). **Passed.**

### Bug Description Parsing

The bug description template at `docs/templates/bug-template.md` defines the following required section heading formats:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to Reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Attachments | `### **Attachments**` |

Parsing the bug description against each required heading:

| Section | Heading | Status |
|---------|---------|--------|
| Issue Description | `### **Issue Description**` | FOUND |
| Steps to Reproduce | `### **Steps to Reproduce**` | MISSING |
| Expected Result | `### **Expected Result**` | MISSING |
| Actual Result | `### **Actual Result**` | FOUND |
| Attachments | `### **Attachments**` | FOUND |

### Found Sections Content

**Issue Description:**
> The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message.

**Actual Result:**
> HTTP 500 Internal Server Error with a stack trace in the response body.

**Attachments:**
> None.

### Missing Sections

The following required sections are **MISSING** from the bug description:

- **Steps to Reproduce**
- **Expected Result**

---

## Validation Error

> Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

---

## Execution Stopped

Execution stopped at **Step 1** because required sections are missing from the bug description.

Per the skill specification:

> "If any Required Section is missing from the Bug description, list the missing sections and inform the user. Stop execution immediately. Do not attempt to investigate an incomplete bug report."

---

## Steps Not Executed

Steps 2 through 7 were **NOT** executed:

- **Step 2 -- Reproduce/Trace**: Not executed. No reproduction or code-path tracing was attempted.
- **Step 3 -- Codebase Investigation**: Not executed. No codebase analysis was performed.
- **Step 4 -- Root Cause Analysis**: Not executed. No root cause comment was posted to Jira.
- **Step 5 -- Generate Task**: Not executed. No Task issue was created in Jira.
- **Step 5b -- Link Task to Bug**: Not executed. No issue link was created.
- **Step 5c -- Post Digest**: Not executed. No description digest comment was posted.
- **Step 6 -- Decomposition Guard**: Not executed. No decomposition assessment was performed.
- **Step 7 -- Report Result**: Not executed. No result summary was generated.

No investigation, no root cause analysis, no task creation, and no Jira modifications were performed.

---

## Recommended Action

The reporter should update ACME-501 to include the missing sections following the template at `docs/templates/bug-template.md`:

1. Add a `### **Steps to Reproduce**` section with numbered steps to reproduce the bug.
2. Add a `### **Expected Result**` section describing the correct expected behavior.

Once the bug description is complete, re-run:

```
/triage-bug ACME-501
```
