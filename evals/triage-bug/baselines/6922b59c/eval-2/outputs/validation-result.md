# Triage Bug — Step 1: Bug Description Validation

## Issue

- **Key**: ACME-501
- **Summary**: API returns 500 on malformed input

## Validation: FAILED

Bug issue ACME-501 is **missing required sections** defined by the Bug template (`docs/templates/bug-template.md`).

### Required sections check

| Required Section | Heading Format | Present |
|---|---|---|
| Issue Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **NO** |
| Expected Result | `### **Expected Result**` | **NO** |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **NO** |
| Attachments | `### **Attachments**` | Yes |

### Missing sections

The following 3 required sections are missing from the Bug description:

1. **Steps to Reproduce** — The bug report does not include steps to reproduce the issue. The template requires a `### **Steps to Reproduce**` section.
2. **Expected Result** — The bug report does not describe the expected behavior. The template requires a `### **Expected Result**` section.
3. **Environment / Version** — The bug report does not specify the environment or version where the bug was observed. The template requires a `### **Environment / Version**` section.

## Action Required

The Bug description for ACME-501 does not conform to the Bug template at `docs/templates/bug-template.md`. The reporter must add the missing sections before triage can proceed.

## Execution Halted

Triage-bug execution **stops at Step 1**. Steps 2 through 5 are **not executed** because the Bug description failed validation. A complete and template-conformant Bug description is a prerequisite for further triage (task breakdown, estimation, linking, and transition).
