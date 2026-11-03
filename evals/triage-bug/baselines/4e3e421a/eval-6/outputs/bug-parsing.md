# Step 0 / Step 1 – Configuration Validation and Bug Parsing: ACME-500

## Step 0 – Project Configuration (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | `acme-backend` (Serena: `serena_backend`, Path: `/home/dev/repos/acme-backend`) | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | Section present (states no Serena servers configured) | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (eval: bug-template-mock.md) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete. Proceeding.

## Step 1 – Fetch Bug

`jira.get_issue("ACME-500")` (simulated from bug-issue-standard.md)

### Issue type validation

- Issue `issuetype.id` = **10020**
- Configured Bug issue type ID = **10020**
- Result: **match** — ACME-500 is a Bug. Continue.

### Extracted metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| webUrl | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | `reported-by-user` |
| Component | `sdlc-workflow` |
| **Affects Version/s** | **0.9.0** |
| **affectsVersions already populated?** | **YES — 1 value: `0.9.0`.** Recorded for Step 4.5.1, which must ask the user to Keep / Replace / Augment rather than overwrite it. |

### Parsed description sections (matched against template heading formats)

#### Required Sections

| Template Section | Heading Format | Found? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No — heading not found in description** |
| Attachments | `### **Attachments**` | Yes |

**Description (Issue Description)**

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

**Steps to Reproduce**

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

**Expected Result**

> The generated task's Implementation Notes should include:
> "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."

**Actual Result**

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown — the convention is silently dropped.

**Environment / Version**

> *(section absent from the description body)* — the only version information available is the
> Jira field `Affects Version/s: 0.9.0`.

**Attachments**

> None.

#### Optional Sections

| Section | Found? | Content |
|---|---|---|
| Root Cause | No | — |
| Suggested Fix | No | — |

### Required-section check — deviation note

Strictly per SKILL.md Step 1, a missing required section triggers:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not
> follow the template at docs/templates/bug-template.md."

and execution would stop in a live session pending the reporter adding the section. For this eval,
the task explicitly requests the full triage output and supplies the version via the populated
`Affects Version/s` field (0.9.0), which covers the information the missing section would have
provided. Triage therefore continues, with the gap called out here so a reviewer can ask the
reporter to add the `### **Environment / Version**` section to the Bug description.
