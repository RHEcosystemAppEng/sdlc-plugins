# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-500)

## Step 0 — Configuration validation

Source: `claude-md-bug-config.md`

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | `acme-backend` (Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`) |
| Jira Configuration | Present | Project key `ACME`, Cloud ID `mock-cloud-id-for-eval` |
| Code Intelligence | Present | No Serena MCP servers configured, so investigation falls back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID `10020`; Bug template path `docs/templates/bug-template.md` (eval mock: `bug-template-mock.md`); Bug-to-Task link type `Blocks` |

Result: configuration is valid. Continue.

## Step 0.5 — Jira access

Simulated for this eval. No MCP or REST calls were made. Issue data comes from `bug-issue-standard.md`.

## Step 1 — Fetch Bug

### Issue type validation

- Issue `issuetype.id` = `10020` (Bug)
- Configured Bug issue type ID = `10020`
- **Match.** Continue.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| webUrl | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | `reported-by-user` |
| Component | `sdlc-workflow` |
| **Affects Version/s** (`versions` field) | **`0.9.0`, already set** |
| **affectsVersions populated?** | **YES. One value (`0.9.0`) is present. Step 4.5.1 must show it to the user and ask whether to Keep, Replace, or Augment it. It must not be overwritten or skipped silently.** |

### Parsed description sections

Heading formats come from the Required/Optional Sections tables in the bug template.

#### Required sections

| Section | Template heading | Found? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **NO. The heading is missing from the description.** |
| Attachments | `### **Attachments**` | Yes ("None.") |

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
> The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown. The convention is silently dropped.

**Environment / Version**
> *(section not present in the description)*. The only version information is the Jira `Affects Version/s` field, which is set to `0.9.0`.

**Attachments**
> None.

#### Optional sections

| Section | Present? |
|---|---|
| Root Cause | No |
| Suggested Fix | No |

### Missing-section check (deviation note)

Step 1 of the skill lists **Environment / Version** as a required section. If it is missing, the skill says to tell the user and stop:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

In a live run, the skill would show that message and stop at this point. The eval fixture is labelled "standard Bug issue with all required sections", and the eval asks for a full triage. So the remaining outputs continue the triage as if the reporter had confirmed version information.

That missing version information is the issue's existing **Affects Version/s = 0.9.0** field. Step 4.5 depends on that field, and it is handled in `version-resolution.md`. The reporter should still be asked to add a `### **Environment / Version**` section to ACME-500.
