# Triage Bug — Validation Result for ACME-501

## Step 1: Configuration Validation and Bug Description Parsing

### Configuration Validation

The skill read the project CLAUDE.md and located the **Bug Configuration** section:

- **Bug issue type ID**: 10020
- **Bug template path**: `docs/templates/bug-template.md`
- **Bug-to-Task link type**: Blocks

The bug issue ACME-501 has issue type `Bug (ID: 10020)`, which matches the configured Bug issue type ID (10020). Configuration validation passed.

### Bug Description Parsing

The skill fetched the bug issue ACME-501 and parsed its description to identify section headings. It then compared the headings found in the bug description against the required sections defined in the bug template at `docs/templates/bug-template.md`.

**Required sections (from the bug template):**

| Section | Heading Format | Present in ACME-501? |
|---------|----------------|----------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No** |
| Expected Result | `### **Expected Result**` | **No** |
| Actual Result | `### **Actual Result**` | Yes |

**Headings found in ACME-501:**
- `### **Issue Description**` — matched required section
- `### **Actual Result**` — matched required section
- `### **Attachments**` — present (optional section, not required for validation)

**Missing required sections:**
1. `### **Steps to Reproduce**`
2. `### **Expected Result**`

### Validation Outcome

**FAILED** — The bug description is missing 2 of 4 required sections.

The skill stopped execution immediately and did not proceed to Step 2 (investigation), Step 3 (root cause analysis), Step 4 (task creation), or Step 5 (status update).

### Error Message

> Triage halted: bug ACME-501 is missing required sections defined in the bug template (`docs/templates/bug-template.md`).
>
> Missing sections:
> - **Steps to Reproduce** (expected heading: `### **Steps to Reproduce**`)
> - **Expected Result** (expected heading: `### **Expected Result**`)
>
> Please update the bug description to include all required sections before re-running triage.
