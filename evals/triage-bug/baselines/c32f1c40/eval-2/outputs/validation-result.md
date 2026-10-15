# Step 1 -- Bug Description Parsing: Validation Result

## Issue

**Key**: ACME-501
**Summary**: API returns 500 on malformed input
**Issue Type**: Bug (ID: 10020)

## Step 0 -- Configuration Validation

Bug Configuration was found in the project CLAUDE.md with all required fields:

- Bug issue type ID: 10020
- Bug template path: `docs/templates/bug-template.md`
- Bug-to-Task link type: Blocks

The issue type ID on ACME-501 (10020) matches the configured Bug issue type ID (10020), so the issue type check passes.

## Step 1 -- Bug Description Parsing

### Template Analysis

The bug description template at `docs/templates/bug-template.md` defines the following **Required Sections**:

| Section              | Heading Format                   |
|----------------------|----------------------------------|
| Description          | `### **Issue Description**`      |
| Steps to Reproduce   | `### **Steps to Reproduce**`     |
| Expected Result      | `### **Expected Result**`        |
| Actual Result        | `### **Actual Result**`          |
| Environment / Version| `### **Environment / Version**`  |
| Attachments          | `### **Attachments**`            |

### Sections Found in ACME-501

The bug description contains only three of the six required sections:

| Section              | Status  |
|----------------------|---------|
| Description          | Present |
| Steps to Reproduce   | **MISSING** |
| Expected Result      | **MISSING** |
| Actual Result        | Present |
| Environment / Version| **MISSING** |
| Attachments          | Present |

### Validation Outcome: FAILED

Three required sections are missing from the bug description. Per the skill definition, execution must stop immediately with the following message:

> Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**, **Environment / Version**. The bug description does not follow the template at `docs/templates/bug-template.md`.

### Action Taken

Execution stopped at Step 1. Steps 2 through 5 were not attempted because the bug report is incomplete. The reporter must update ACME-501 to include the missing sections before triage can proceed.
