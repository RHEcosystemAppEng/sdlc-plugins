# Step 1 – Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Extracted from `claude-md-bug-config.md`:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required CLAUDE.md sections present. Proceeding.

---

## Issue Metadata

| Field | Value |
|---|---|
| Key | ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |

**Issue type validation**: Issue type ID 10020 matches Bug Configuration Bug issue type ID (10020). ✓

**Affects Version field**: Already populated (`0.9.0`). Step 4.5 will present the Keep/Replace/Augment prompt.

---

## Required Section Validation

Template required sections (from `bug-template-mock.md`):

| Section | Heading Format | Present? |
|---------|----------------|----------|
| Description | `### **Issue Description**` | Yes ✓ |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes ✓ |
| Expected Result | `### **Expected Result**` | Yes ✓ |
| Actual Result | `### **Actual Result**` | Yes ✓ |
| Environment / Version | `### **Environment / Version**` | Not in description body — version available from Jira metadata field (Affects Version/s: 0.9.0) |
| Attachments | `### **Attachments**` | Yes ✓ |

**Note on Environment / Version**: The `### **Environment / Version**` heading is absent from the description body. However, version information is present in the Jira metadata `Affects Version/s` field (value: 0.9.0). This is treated as satisfying the version requirement for triage purposes. The Affects Version/s field will be handled in Step 4.5.

---

## Parsed Required Sections

### Description

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `), the plan-feature skill's convention conformance analysis fails to match the heading and silently skips the convention. No warning is logged. The generated task description omits the convention that should have been included.

### Steps to Reproduce

> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

### Expected Result

> The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.

### Environment / Version

Not present as a description section. Version sourced from metadata: **0.9.0** (from Affects Version/s field).

### Attachments

> None.

---

## Optional Sections

| Section | Present? | Content |
|---------|----------|---------|
| Root Cause | No | — |
| Suggested Fix | No | — |

No optional sections provided by the reporter. Root cause will be determined via investigation (Steps 2–3).
