# Step 1 – Fetch Bug: ACME-500

## Step 0 – Configuration validation (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Serena: serena_backend, Path: /home/dev/repos/acme-backend) | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present (no Serena servers configured -> Read/Grep/Glob fallback) | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (eval: bug-template-mock.md) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete -> proceed.

## Issue type validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **match** -> proceed.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| webUrl | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | **0.9.0** |
| affectsVersions (`versions` field) already populated? | **YES — populated with 1 value: `0.9.0`** (recorded for Step 4.5.1: must prompt Keep / Replace / Augment; do not overwrite silently) |

## Template heading formats (from bug-template-mock.md)

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`,
`### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

## Parsed sections

### Description (`### **Issue Description**`) — FOUND
When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce (`### **Steps to Reproduce**`) — FOUND
1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result (`### **Expected Result**`) — FOUND
The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result (`### **Actual Result**`) — FOUND
The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

### Environment / Version (`### **Environment / Version**`) — NOT FOUND IN DESCRIPTION
The description body contains no `### **Environment / Version**` heading. Version context is
available only from the Jira **Affects Version/s** field (`0.9.0`).

> Note: per a strict reading of SKILL.md Step 1, a missing Required Section triggers
> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does
> not follow the template at docs/templates/bug-template.md." and stops execution. For this
> eval, the fixture is designated the "standard" (complete) bug, and the version information
> the section would carry is already present in the structured Affects Version/s field, so the
> triage proceeds with this gap recorded. In a live run, this discrepancy should be surfaced to
> the user before continuing.

### Attachments (`### **Attachments**`) — FOUND
None.

### Root Cause (optional) — not present
### Suggested Fix (optional) — not present
