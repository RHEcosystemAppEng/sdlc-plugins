# Triage Bug - Step 1 Validation Result

## Issue: ACME-501

**Summary**: API returns 500 on malformed input
**Status**: New
**Component**: api-gateway

## Step 0 - Configuration Validation

Configuration validated successfully. Extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 - Fetch Bug and Parse Description

### Issue Type Validation

The issue type ID (10020) matches the Bug issue type ID from Bug Configuration (10020). Validation passed.

### Bug Description Parsing

The bug description template at `docs/templates/bug-template.md` defines the following **Required Sections**:

| Section | Heading Format | Present in ACME-501? |
|---------|----------------|----------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No - MISSING** |
| Expected Result | `### **Expected Result**` | **No - MISSING** |
| Actual Result | `### **Actual Result**` | Yes |
| Attachments | `### **Attachments**` | Yes |

The bug description was parsed by matching each required heading format from the template against the headings present in the ACME-501 description. The following headings were found:

- `### **Issue Description**` - matched, content extracted
- `### **Actual Result**` - matched, content extracted
- `### **Attachments**` - matched, content extracted

The following required headings were **not found** anywhere in the description:

- `### **Steps to Reproduce**`
- `### **Expected Result**`

### Validation Outcome: FAILED

Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

**Execution stopped immediately.** Per the triage-bug skill specification (Step 1), when any required section is missing from the bug description, the skill must halt and not proceed to Steps 2-5. An incomplete bug report does not provide the structured input needed for reproduction, codebase investigation, root cause analysis, or task generation.

### Action Required

The reporter must update ACME-501's description to include all required sections per the bug template at `docs/templates/bug-template.md`:

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) - The specific steps to trigger the bug (e.g., the exact malformed JSON payload and API endpoint used).
2. **Expected Result** (`### **Expected Result**`) - What the reporter expected to happen (e.g., HTTP 400 Bad Request with a descriptive error message).

Once the description is updated, re-run `/triage-bug ACME-501` to proceed with triage.
