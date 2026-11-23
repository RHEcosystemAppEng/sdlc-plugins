# Step 1 – Fetch Bug: ACME-500

## Step 0 – Configuration validated (from claude-md-bug-config.md)

| Item | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md (simulated by bug-template-mock.md) |
| Bug-to-Task link type | Blocks |
| Repository Registry | acme-backend — Serena instance `serena_backend` — `/home/dev/repos/acme-backend` |
| Code Intelligence | No Serena MCP servers configured, so I fall back to Read/Grep/Glob (simulated by repo-context-mock.md) |

## Issue type validation

- Issue `issuetype.id` = **10020**
- Configured Bug issue type ID = **10020**
- Result: **match**. ACME-500 is a Bug, so triage continues.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | `reported-by-user` |
| Component | sdlc-workflow |
| **Affects Version/s** | **0.9.0** |
| **affectsVersions (`versions` field) already populated?** | **YES: 1 value (`0.9.0`).** Recorded for Step 4.5.1, which will ask the user to Keep / Replace / Augment. The field will not be silently overwritten. |

## Parsed description sections (matched against the template headings)

### Required sections

| Template section | Heading format | Present? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No (heading not found in the description)** |
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
No warning or error is shown. The convention is silently dropped.

#### Environment / Version
*(Section not present in the description.)* The only version information on the issue is
the Jira **Affects Version/s** field, which is set to `0.9.0`.

#### Attachments
None.

### Optional sections

| Section | Present? | Content |
|---|---|---|
| Root Cause | No | — |
| Suggested Fix | No | — |

## Template-completeness note

Under a strict reading of Step 1, a missing Required Section means the skill stops with this message:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not
> follow the template at docs/templates/bug-template.md."

In this eval run I flag the gap but continue. The eval asks for the full triage, and the
missing section's purpose (giving version context) is already covered by the populated
Affects Version/s field (`0.9.0`). In a live run I would tell the user about the gap first,
and I would recommend that the reporter add a `### **Environment / Version**` section.
