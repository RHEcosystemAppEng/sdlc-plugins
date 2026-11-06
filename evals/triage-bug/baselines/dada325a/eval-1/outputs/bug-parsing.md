# Step 1 – Fetch Bug: Parsing Result for ACME-500

## Step 0 – Configuration Validation (passed)

| Item | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md (mock: bug-template-mock.md) |
| Bug-to-Task link type | Blocks |
| Repository Registry | acme-backend (serena_backend, /home/dev/repos/acme-backend) |
| Code Intelligence | Section present (no Serena servers configured) |

## Issue Type Validation (passed)

- Issue `issuetype.id` = 10020, which matches the configured Bug issue type ID 10020.

## Metadata

- **Key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s field**: 0.9.0 (populated)

## Required Sections (from template)

| Section | Expected Heading | Found? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **NO, MISSING** |
| Attachments | `### **Attachments**` | Yes ("None.") |

## Optional Sections

| Section | Found? |
|---|---|
| Root Cause | No |
| Suggested Fix | No |

## Extracted Content

### Description
When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce
1. Create a `CONVENTIONS.md` with a heading that has trailing whitespace: `## Migration Patterns  ` followed by `Add Index::create() for all FK columns.`
2. Run `/plan-feature ACME-100` on a feature that needs a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result
Implementation Notes include: "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."

### Actual Result
Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown.

### Environment / Version
**MISSING.** The description has no `### **Environment / Version**` section. The Jira
`Affects Version/s` field is set to 0.9.0, but that field does not stand in for the required
description section.

## Validation Outcome: STOP

Message to user (per Step 1):

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not
> follow the template at docs/templates/bug-template.md."

**Execution stopped at Step 1.** Per the skill: "Stop execution immediately. Do not attempt to
investigate an incomplete bug report." Steps 2–7 (investigation, root cause comment, Affects
Version resolution, Task creation, linking, digest) were NOT performed.

Recommended next action: the reporter adds a `### **Environment / Version**` section to ACME-500
(e.g., "sdlc-workflow plugin 0.9.0, Claude Code <version>"), then re-runs `/triage-bug ACME-500`.
