# Triage Bug ACME-501: Validation Result

## Outcome

**Execution STOPPED at Step 1 (Fetch Bug, Parse bug description).** The Bug description is missing required sections, so no investigation, root cause analysis, Task creation, linking, or Jira comments happened.

Message shown to the user:

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

## Step 0: Validate Project Configuration (PASSED)

The project CLAUDE.md (claude-md-bug-config.md) has every required section:

| Section | Status | Values extracted |
|---|---|---|
| Repository Registry | Present (1 entry) | acme-backend, serena_backend, /home/dev/repos/acme-backend |
| Jira Configuration | Present | Project key: ACME, Cloud ID: mock-cloud-id-for-eval |
| Code Intelligence | Present | (no Serena servers configured) |
| Bug Configuration | Present | Bug issue type ID: 10020, Bug template path: docs/templates/bug-template.md, Bug-to-Task link type: Blocks |

## Step 0.5: Jira Access

Skipped for this eval because no external services are called. The issue content came from bug-issue-missing-sections.md.

## Step 1: Fetch Bug

### Issue type validation (PASSED)

- Issue `issuetype.id`: 10020 (Bug)
- Configured Bug issue type ID: 10020
- They match, so parsing continued.

### Bug description parsing (FAILED)

The template (bug-template-mock.md) was read. Its Required and Optional Sections tables give these heading formats. The issue description was matched against them:

#### Required sections

| Section | Expected heading | Found in ACME-501? |
|---|---|---|
| Description | `### **Issue Description**` | Present: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message." |
| Steps to Reproduce | `### **Steps to Reproduce**` | **MISSING** |
| Expected Result | `### **Expected Result**` | **MISSING** |
| Actual Result | `### **Actual Result**` | Present: "HTTP 500 Internal Server Error with a stack trace in the response body." |
| Environment / Version | `### **Environment / Version**` | **MISSING** |
| Attachments (template only) | `### **Attachments**` | Present: "None." |

Note: The skill's required-section list has five sections (Description, Steps to Reproduce, Expected Result, Actual Result, Environment / Version). The mock template also lists Attachments as required. It is present either way, so it does not change the result.

Note: The issue summary hints at what the expected behavior is ("should return 400 Bad Request"). It was not used to fill in Expected Result. The skill says not to guess or investigate an incomplete bug report.

#### Optional sections

| Section | Expected heading | Found? |
|---|---|---|
| Root Cause | `### **Root Cause**` | Not present (optional, no effect) |
| Suggested Fix | `### **Suggested Fix**` | Not present (optional, no effect) |

### Result

Three required sections are missing:

1. **Steps to Reproduce**
2. **Expected Result**
3. **Environment / Version**

The skill says: "If any Required Section is missing from the Bug description, list the missing sections and inform the user ... **Stop execution immediately.** Do not attempt to investigate an incomplete bug report."

The skill stopped here as instructed.

## Steps NOT executed

- Step 1 metadata extraction (only the fields above were recorded, for context)
- Step 2: Reproduce/Trace (needs Steps to Reproduce, which is missing)
- Step 3: Codebase Investigation
- Step 4: Root Cause Analysis (no comment posted on ACME-501)
- Step 4.5: Affects Version Resolution (needs Environment / Version, which is missing)
- Step 5 / 5b / 5c: No Task created, no link added, no digest posted
- Step 6: Decomposition Guard
- Step 7: Report Result (only the validation failure was reported)

## Recommended next action

The reporter should update ACME-501 to add `### **Steps to Reproduce**`, `### **Expected Result**`, and `### **Environment / Version**` sections, following docs/templates/bug-template.md. Then re-run `/triage-bug ACME-501`.
