# Triage Bug — Validation Result

## Bug: ACME-501

### Step 0 — Validate Configuration

Bug Configuration found in CLAUDE.md:

- Bug issue type ID: 10020
- Bug template path: docs/templates/bug-template.md
- Bug-to-Task link type: Blocks

Configuration is valid.

### Step 1 — Fetch and Validate Bug Description

**Issue type check**: ACME-501 has issue type Bug (ID: 10020), which matches the configured Bug issue type ID (10020). Passed.

**Template parsing**: Read the bug template at docs/templates/bug-template.md. The template defines the following required sections:

| # | Required Section | Heading Format | Present in Bug? |
|---|---|---|---|
| 1 | Description | `### **Issue Description**` | Yes |
| 2 | Steps to Reproduce | `### **Steps to Reproduce**` | **No** |
| 3 | Expected Result | `### **Expected Result**` | **No** |
| 4 | Actual Result | `### **Actual Result**` | Yes |
| 5 | Environment / Version | `### **Environment / Version**` | **No** |
| 6 | Attachments | `### **Attachments**` | Yes |

**Result: VALIDATION FAILED**

Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md.

Execution stopped. Steps 2-5 were not performed.
