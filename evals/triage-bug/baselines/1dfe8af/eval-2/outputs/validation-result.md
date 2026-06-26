# Validation Result: Bug ACME-501 Description Parsing (Step 1)

## Overview

Triage of Bug ACME-501 ("API returns 500 on malformed input") was attempted following the triage-bug skill process. Execution halted at Step 1 (Fetch Bug) during bug description parsing because the bug report is missing required sections defined by the bug description template.

## Step 0 -- Validate Project Configuration

Configuration validated successfully from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: `docs/templates/bug-template.md`
- **Bug-to-Task link type**: Blocks

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration) are present and complete.

## Step 1 -- Fetch Bug

### Issue type validation

The issue's type ID (10020) matches the Bug issue type ID from Bug Configuration (10020). Issue type validation passed.

### Bug description parsing

The bug description template at `docs/templates/bug-template.md` defines the following **Required Sections**:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Attachments | `### **Attachments**` |

The bug description of ACME-501 was parsed against these required heading formats. The following sections were **found** in the description:

- `### **Issue Description**` -- present, with content: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
- `### **Actual Result**` -- present, with content: "HTTP 500 Internal Server Error with a stack trace in the response body."
- `### **Attachments**` -- present, with content: "None."

The following **Required Sections are missing** from the description:

1. **Steps to Reproduce** (expected heading: `### **Steps to Reproduce**`) -- not found anywhere in the bug description
2. **Expected Result** (expected heading: `### **Expected Result**`) -- not found anywhere in the bug description

## Result

> Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

**Execution stopped.** Per the triage-bug skill SKILL.md Step 1 rules: "If any Required Section is missing from the Bug description, list the missing sections and inform the user. Stop execution immediately. Do not attempt to investigate an incomplete bug report."

Steps 2 through 7 (Reproduce/Trace, Codebase Investigation, Root Cause Analysis, Generate Task, Link Task, Post Digest, Decomposition Guard, Report Result) were **not executed**.

## Action Required

The reporter must update Bug ACME-501 to include the missing sections before triage can proceed:

1. Add a `### **Steps to Reproduce**` section with the steps to trigger the 500 error (e.g., the specific malformed JSON payload and API endpoint).
2. Add a `### **Expected Result**` section describing the expected behavior (e.g., HTTP 400 Bad Request with a descriptive error message).

Once the bug description is complete, re-run `/triage-bug ACME-501`.
