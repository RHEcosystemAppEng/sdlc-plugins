# Step 1 – Fetch Bug: ACME-500

## Step 0 – Configuration (validated)

| Item | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md (eval mock: bug-template-mock.md) |
| Bug-to-Task link type | Blocks |
| Repository Registry | acme-backend (Serena instance: serena_backend, path /home/dev/repos/acme-backend) |
| Code Intelligence | Section present; no Serena MCP servers configured (fallback: Read/Grep/Glob) |

All required configuration sections are present. Proceeding to Step 1.

## Issue type validation

- Issue type: Bug (ID: 10020)
- Configured Bug issue type ID: 10020
- Result: **match** — issue is a Bug.

## Metadata

| Field | Value |
|---|---|
| Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s (Jira field) | 0.9.0 (already populated) |

## Parsed description sections (matched against template heading formats)

### Required sections

| Section | Template heading | Found? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **NO — MISSING** |
| Attachments | `### **Attachments**` | Yes |

#### Description
When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce
1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result
The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result
The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

#### Environment / Version
**Not present in the description.** (The Jira `Affects Version/s` field is set to `0.9.0`, but
that is issue metadata, not the required `### **Environment / Version**` description section.)

#### Attachments
None.

### Optional sections

| Section | Template heading | Found? |
|---|---|---|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

## Result: execution stopped

Per SKILL.md Step 1 ("If any Required Section is missing from the Bug description ... Stop
execution immediately. Do not attempt to investigate an incomplete bug report."), triage halts here.

Message presented to the user:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not
> follow the template at docs/templates/bug-template.md."

Suggested remediation for the user: add a `### **Environment / Version**` section to the ACME-500
description (for example, the sdlc-workflow plugin version, e.g. 0.9.0, and the Claude Code
version), then re-run `/triage-bug ACME-500`.
