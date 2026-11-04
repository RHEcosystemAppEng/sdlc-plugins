# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-500)

## Step 0 — Configuration validation (from claude-md-bug-config.md)

| Section | Status | Values extracted |
|---|---|---|
| Repository Registry | present | `acme-backend` — Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | present | Project key: `ACME`; Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | present | No Serena MCP servers configured — fall back to Read/Grep/Glob |
| Bug Configuration | present | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md` (eval mock: `bug-template-mock.md`); Bug-to-Task link type: `Blocks` |

Result: configuration is valid, so the skill continues.

## Step 0.5 — Jira access

Not run, per the eval instructions (no MCP or REST calls). The issue data comes from `bug-issue-standard.md`.

## Step 1 — Fetch Bug

### Issue type validation

- Issue `issuetype.id` = `10020` (Bug)
- Configured Bug issue type ID = `10020`
- **Match.** The issue is a Bug, so the skill continues.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | `reported-by-user` |
| Component | `sdlc-workflow` |
| Affects Version/s | `0.9.0` |
| **affectsVersions already populated?** | **YES — 1 value (`0.9.0`).** Recorded so Step 4.5.1 offers Keep / Replace / Augment and does not overwrite the field without asking. |

### Parsed description sections (matched against the template heading formats)

#### Required sections

| Template section | Heading format | Found? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **NO — heading not present in description** |
| Attachments | `### **Attachments**` | Yes (content: "None.") |

**Description**
> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `), the plan-feature skill's convention conformance analysis fails to match the heading and silently skips the convention. No warning is logged. The generated task description omits the convention that should have been included.

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
> The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.

**Environment / Version**
> *(section missing from the description body)*. The only version information is in the Jira field **Affects Version/s: 0.9.0**.

**Attachments**
> None.

#### Optional sections

| Section | Found? | Content |
|---|---|---|
| Root Cause | No | — |
| Suggested Fix | No | — |

### Required-section check — message to user

Strictly, SKILL.md Step 1 treats a missing required section as a hard stop. The skill would show this message:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

**Note on how this eval run continues:** the eval task asks for all downstream outputs, and the version information this section would hold already exists in the issue's Affects Version/s field (`0.9.0`). So the later steps are written as the triage that would run once the reporter adds the section, or the user accepts the Affects Version/s field as the environment/version source. In a live run the skill would stop here until the description is fixed. Steps 2–5 below assume the Environment / Version information is `0.9.0`, taken from the existing Jira field.
