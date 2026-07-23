# Validation Result -- ACME-501 Bug Description Parsing (Step 1)

## Outcome: STOP -- Incomplete Bug Report

Execution halted at Step 1 (Parse bug description). The bug description does not
conform to the required template and cannot be triaged.

## Step 0 -- Validate Project Configuration

Configuration validation **passed**. All required sections found in CLAUDE.md:

| Section | Status | Extracted Value |
|---------|--------|-----------------|
| Repository Registry | Present | acme-backend (Rust backend service) |
| Jira Configuration | Present | Project key: ACME, Cloud ID: mock-cloud-id-for-eval |
| Code Intelligence | Present | No Serena instances configured |
| Bug Configuration | Present | Bug issue type ID: 10020, Bug template path: docs/templates/bug-template.md, Bug-to-Task link type: Blocks |

## Step 1 -- Fetch Bug

### Issue Type Validation

**Passed.** The issue type ID on ACME-501 is 10020, which matches the Bug issue type
ID (10020) from Bug Configuration.

### Bug Description Parsing

The bug template at `docs/templates/bug-template.md` defines the following required
and optional sections:

**Required Sections (from template):**

| # | Section | Expected Heading | Present in ACME-501 |
|---|---------|-----------------|---------------------|
| 1 | Description | `### **Issue Description**` | Yes |
| 2 | Steps to reproduce | `### **Steps to Reproduce**` | No |
| 3 | Expected Result | `### **Expected Result**` | No |
| 4 | Actual Result | `### **Actual Result**` | Yes |
| 5 | Environment / Version | `### **Environment / Version**` | No |
| 6 | Attachments | `### **Attachments**` | Yes |

**Optional Sections (from template):**

| # | Section | Expected Heading | Present in ACME-501 |
|---|---------|-----------------|---------------------|
| 1 | Root Cause | `### **Root Cause**` | No |
| 2 | Suggested Fix | `### **Suggested Fix**` | No |

### Sections Found in ACME-501

The following three sections were successfully parsed from the bug description:

1. **Issue Description** -- "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. **Actual Result** -- "HTTP 500 Internal Server Error with a stack trace in the response body."
3. **Attachments** -- "None."

### Missing Required Sections

Three required sections are absent from the ACME-501 description:

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) -- No heading matching this format exists in the description. Without reproduction steps, the bug cannot be traced or reproduced in Step 2.
2. **Expected Result** (`### **Expected Result**`) -- No heading matching this format exists in the description. Without the expected result, there is no baseline to compare against during investigation.
3. **Environment / Version** (`### **Environment / Version**`) -- No heading matching this format exists in the description. Without environment/version information, Step 4.5 (Affects Version Resolution) cannot extract version identifiers.

### Action Taken

Per SKILL.md Step 1 rules:

> "If any Required Section is missing from the Bug description, list the missing
> sections and inform the user. **Stop execution immediately.** Do not attempt to
> investigate an incomplete bug report."

The skill stops and reports to the user:

> Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result,
> Environment / Version. The bug description does not follow the template at
> docs/templates/bug-template.md.

No further steps (Steps 2 through 7) are executed. The reporter must update the bug
description to include all required sections before triage can proceed.

### Metadata Extracted (Before Stop)

Although execution stops, the following metadata was extracted from the issue:

- **Issue key**: ACME-501
- **Web URL**: https://mock-jira.example.com/browse/ACME-501
- **Summary**: API returns 500 on malformed input
- **Labels**: production-incident
- **Component**: api-gateway
- **Affects Version/s**: Not set
