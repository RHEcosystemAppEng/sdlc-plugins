# Step 1 – Fetch Bug: Parsed Description

## Step 0 – Configuration Validation

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Serena instance: serena_backend, path: /home/dev/repos/acme-backend) | Present |
| Project key | ACME | Present |
| Cloud ID | mock-cloud-id-for-eval | Present |
| Code Intelligence | Section present; no Serena MCP servers configured, so Read/Grep/Glob is the fallback | Present |
| Bug issue type ID | 10020 | Present |
| Bug template path | docs/templates/bug-template.md (mock: bug-template-mock.md) | Present |
| Bug-to-Task link type | Blocks | Present |

The configuration is valid, so the skill can continue.

## Issue Type Validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **Match.** ACME-500 is a Bug, so triage can continue.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 (the `versions` field **is already populated**) |

## Required Sections (matched against template heading formats)

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
No warning or error is shown. The convention is silently dropped.

### Environment / Version (`### **Environment / Version**`) — NOT FOUND IN DESCRIPTION

The description has no `### **Environment / Version**` heading. The version is available from
the Jira **Affects Version/s** field (`0.9.0`). The description does not state any environment,
such as OS or Claude Code version.

> **Template conformance flag:** Under a strict reading of Step 1, a missing required section
> means telling the user and stopping:
> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not
> follow the template at docs/templates/bug-template.md."
>
> In this eval run, triage continued for two reasons. The Jira Affects Version/s field already
> gives the version (0.9.0). The remaining required sections fully specify the bug's behavior.
> In a live run the reporter should be asked to add the Environment / Version section to the description.

### Attachments (`### **Attachments**`) — FOUND

None.

## Optional Sections

| Section | Status |
|---|---|
| Root Cause (`### **Root Cause**`) | Not present: the reporter gave no prior analysis |
| Suggested Fix (`### **Suggested Fix**`) | Not present: the reporter gave no proposed solution |
